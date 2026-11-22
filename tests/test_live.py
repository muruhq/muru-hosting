"""The stream of a site's log and events, and the view that hands a request to it."""

import asyncio
from collections.abc import MutableMapping
from typing import Any

from django.test import Client
from muruhosting_stubs.muru.admin.v1 import admin_pb2

from hub.accounts.models import User
from hub.hosting import live
from hub.hosting.models import Site
from tests.conftest import RunningSite


class Bridge:
    """Stand in for what Muru puts in a WSGI environ to hand a request to ASGI."""

    def __init__(self, enabled: bool = True) -> None:
        self.scope: dict[str, Any] = {"state": {}}
        self.handed_to: object = None
        self._enabled = enabled

    def handoff(self, app: object) -> None:
        """Take the application the request goes on as, or refuse as Muru does."""

        if not self._enabled:
            raise RuntimeError("the entrypoint does not enable handing requests to ASGI")

        self.handed_to = app


def test_the_stream_view_hands_the_request_on_with_the_sites_helper(
    client: Client, site: Site, member: User
) -> None:
    bridge = Bridge()
    client.force_login(member)

    response = client.get("/sites/alice/blog/stream/", **{"muru.wsgi_to_asgi": bridge})  # type: ignore[arg-type]

    assert response.status_code == 200
    assert bridge.handed_to is live.site_stream
    assert bridge.scope["state"] == {"helper_address": "127.0.0.1:1", "helper_token": "token"}


def test_the_stream_is_not_handed_on_for_a_site_someone_may_not_see(
    client: Client, site: Site
) -> None:
    bridge = Bridge()
    client.force_login(User.objects.create_user("bob", password="correct horse"))

    response = client.get("/sites/alice/blog/stream/", **{"muru.wsgi_to_asgi": bridge})  # type: ignore[arg-type]

    assert response.status_code == 404
    assert bridge.handed_to is None


def test_a_hub_that_cannot_stream_says_so(client: Client, site: Site, member: User) -> None:
    client.force_login(member)

    assert client.get("/sites/alice/blog/stream/").status_code == 501

    refusing = client.get("/sites/alice/blog/stream/", **{"muru.wsgi_to_asgi": Bridge(False)})  # type: ignore[arg-type]

    assert refusing.status_code == 501


def test_an_event_of_several_lines_is_one_server_sent_event() -> None:
    assert live.sse("log", "one\ntwo") == b"event: log\ndata: one\ndata: two\n\n"
    assert live.sse("changed") == b"event: changed\ndata: \n\n"


def test_an_event_is_written_as_the_page_reads_it() -> None:
    event = admin_pb2.Event(sequence=7, time_unix_ms=1000, type="release.ready", subject="site@r2")

    assert '"sequence": 7' in live.event_json(event)
    assert '"type": "release.ready"' in live.event_json(event)


def test_the_stream_follows_a_real_site_until_the_browser_goes_away(
    running_site: RunningSite,
) -> None:
    sent: list[MutableMapping[str, Any]] = []
    scope = {
        "type": "http",
        "state": {
            "helper_address": running_site.helper_address,
            "helper_token": running_site.token,
        },
    }

    async def follow() -> None:
        gone = asyncio.Event()

        async def receive() -> MutableMapping[str, Any]:
            await gone.wait()

            return {"type": "http.disconnect"}

        async def send(message: MutableMapping[str, Any]) -> None:
            sent.append(message)

            if b"log-reset" in message.get("body", b""):
                gone.set()

        await asyncio.wait_for(live.site_stream(scope, receive, send), timeout=30)

    asyncio.run(follow())

    assert sent[0]["type"] == "http.response.start"
    assert (b"content-type", b"text/event-stream; charset=utf-8") in sent[0]["headers"]
    assert any(b"event: log-reset" in message.get("body", b"") for message in sent)
