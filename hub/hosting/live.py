"""A site's log and events streamed to its page as they happen.

Specification section 2.1. A view checks who is asking, then hands the
request to `site_stream` on the worker's event loop (Muru's handoff), so a
stream that stays open for as long as the page does holds no WSGI thread.
The stream is Server-Sent Events:

- `log-reset`, then `log` for each line of the serving release's log, the
  last hundred first;

- `event` for each of the daemon's events, the last thirty first, as JSON;

- `changed` when an event arrives after those, for the page to ask the hub
  again for the part of it that the event may have changed.

The calls to the helper here are gRPC's asyncio calls, apart from the
client in `helper.py`, which serves the hub's ordinary requests and jobs.
"""

from __future__ import annotations

import asyncio
import contextlib
import json
from collections.abc import Awaitable, Callable, MutableMapping
from typing import Any

import grpc
import grpc.aio
from muruhosting_stubs.muru.admin.v1 import admin_pb2, admin_pb2_grpc

from hub.hosting.models import APP

Scope = MutableMapping[str, Any]
Receive = Callable[[], Awaitable[MutableMapping[str, Any]]]
Send = Callable[[MutableMapping[str, Any]], Awaitable[None]]

LOG_LINES = 100
EVENTS = 30

# How often a comment is sent on a quiet stream, so that the edge, and any
# proxy in front of it, sees the response is alive.

HEARTBEAT = 15.0

# How long to wait before asking again after the log could not be read, as
# it cannot be before a site's first release.

RETRY = 3.0

# The events after which the serving release, and so the log to follow, may
# be another.

SWITCHES = frozenset({"traffic.switched"})


def sse(event: str, data: str = "") -> bytes:
    """Write one Server-Sent Event, whose data may run to several lines."""

    lines = "".join(f"data: {line}\n" for line in data.split("\n"))

    return f"event: {event}\n{lines}\n".encode()


def event_json(event: admin_pb2.Event) -> str:
    """Write one of the daemon's events as the page reads it."""

    return json.dumps(
        {
            "sequence": event.sequence,
            "time": event.time_unix_ms,
            "type": event.type,
            "subject": event.subject,
            "level": event.level,
            "message": event.message,
        }
    )


class SiteFeed:
    """What one open page is sent about one site."""

    def __init__(self, address: str, token: str) -> None:
        self._address = address
        self._metadata = (("authorization", f"Bearer {token}"),)
        self._queue: asyncio.Queue[bytes] = asyncio.Queue(maxsize=1000)
        self._log: asyncio.Task[None] | None = None

    async def run(self, send: Send) -> None:
        """Send the stream until the task is cancelled, which the page going away does."""

        async with grpc.aio.insecure_channel(self._address) as channel:
            stub = admin_pb2_grpc.AdminStub(channel)
            events = asyncio.create_task(self._events(stub))
            self._follow_log(stub)

            try:
                while True:
                    try:
                        chunk = await asyncio.wait_for(self._queue.get(), HEARTBEAT)
                    except TimeoutError:
                        chunk = b": still here\n\n"

                    await send({"type": "http.response.body", "body": chunk, "more_body": True})
            finally:
                events.cancel()

                if self._log is not None:
                    self._log.cancel()

    def _follow_log(self, stub: admin_pb2_grpc.AdminStub) -> None:
        """Start following the serving release's log, in place of any log followed before."""

        if self._log is not None:
            self._log.cancel()

        self._log = asyncio.create_task(self._tail(stub))

    async def _tail(self, stub: admin_pb2_grpc.AdminStub) -> None:
        """Send the serving release's log, from its last lines on, for as long as it can be read."""

        while True:
            await self._queue.put(sse("log-reset"))
            tail = stub.TailLogs(
                admin_pb2.TailLogsRequest(app=APP, lines=LOG_LINES, follow=True),
                metadata=self._metadata,
            )

            # The stream ends when the release does, and fails while the
            # site has no release: either way, ask again in a while.

            with contextlib.suppress(grpc.aio.AioRpcError):
                async for entry in tail:
                    await self._queue.put(sse("log", entry.line))

            await asyncio.sleep(RETRY)

    async def _events(self, stub: admin_pb2_grpc.AdminStub) -> None:
        """Send the daemon's latest events, then each new one as it is recorded."""

        while True:
            after = 0

            try:
                # Every kept event is read to send the newest
                # (muruhq/muru#870; #38 here).

                listed = await stub.ListEvents(
                    admin_pb2.ListEventsRequest(), metadata=self._metadata
                )

                for event in listed.events[-EVENTS:]:
                    await self._queue.put(sse("event", event_json(event)))

                if listed.events:
                    after = listed.events[-1].sequence

                watch = stub.WatchEvents(
                    admin_pb2.WatchEventsRequest(after=after), metadata=self._metadata
                )

                async for event in watch:
                    await self._queue.put(sse("event", event_json(event)))
                    await self._queue.put(sse("changed"))

                    if event.type in SWITCHES:
                        self._follow_log(stub)
            except grpc.aio.AioRpcError:
                pass

            await asyncio.sleep(RETRY)


async def site_stream(scope: Scope, receive: Receive, send: Send) -> None:
    """Serve a site's stream: the ASGI application a view hands the request to.

    The view puts the site's helper address and token in the scope's state,
    having checked that the person may see the site.
    """

    feed = SiteFeed(scope["state"]["helper_address"], scope["state"]["helper_token"])

    await send(
        {
            "type": "http.response.start",
            "status": 200,
            "headers": [
                (b"content-type", b"text/event-stream; charset=utf-8"),
                (b"cache-control", b"no-cache"),
            ],
        }
    )

    # The stream runs until the browser goes away, which is the one thing
    # the request still has to say.

    stream = asyncio.create_task(feed.run(send))

    try:
        while not stream.done():
            message = await receive()

            if message["type"] == "http.disconnect":
                break
    finally:
        stream.cancel()

        with contextlib.suppress(asyncio.CancelledError, OSError):
            await stream


async def run_stream(scope: Scope, receive: Receive, send: Send) -> None:
    """Serve the output of one run of a command, and end when the run does.

    The events are `log-reset`, `log` for each line, the last five hundred
    first, and `finished` once the run has ended, after which the response
    is complete and the page stops listening.
    """

    address, token = scope["state"]["helper_address"], scope["state"]["helper_token"]
    metadata = (("authorization", f"Bearer {token}"),)

    await send(
        {
            "type": "http.response.start",
            "status": 200,
            "headers": [
                (b"content-type", b"text/event-stream; charset=utf-8"),
                (b"cache-control", b"no-cache"),
            ],
        }
    )

    async def body(chunk: bytes, more: bool = True) -> None:
        await send({"type": "http.response.body", "body": chunk, "more_body": more})

    async def follow() -> None:
        async with grpc.aio.insecure_channel(address) as channel:
            stub = admin_pb2_grpc.AdminStub(channel)
            await body(sse("log-reset"))
            tail = stub.TailCommandRun(
                admin_pb2.TailCommandRunRequest(run=scope["state"]["run"], lines=500, follow=True),
                metadata=metadata,
            )

            with contextlib.suppress(grpc.aio.AioRpcError):
                async for entry in tail:
                    await body(sse("log", entry.line))

        await body(sse("finished"), more=False)

    # The output is followed until the run ends or the browser goes away,
    # whichever is first.

    stream = asyncio.create_task(follow())
    gone = asyncio.create_task(_disconnected(receive))
    await asyncio.wait({stream, gone}, return_when=asyncio.FIRST_COMPLETED)

    for task in (stream, gone):
        task.cancel()

        with contextlib.suppress(asyncio.CancelledError, OSError):
            await task


async def _disconnected(receive: Receive) -> None:
    """Return once the browser has gone away."""

    while True:
        message = await receive()

        if message["type"] == "http.disconnect":
            return
