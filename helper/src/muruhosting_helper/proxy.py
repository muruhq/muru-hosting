"""The proxy of muru.admin.v1: each allowed call forwarded to the admin socket unchanged.

Specification section 4.1. The proxy is generic over the service's
descriptor: messages pass through as bytes, streams included, so a new Muru
call needs only an entry in the allowlist.
"""

from __future__ import annotations

from collections.abc import AsyncIterator, Awaitable, Callable
from typing import Any

import grpc
import grpc.aio
from muruhosting_stubs.muru.admin.v1 import admin_pb2

from muruhosting_helper import allowlist, auth
from muruhosting_helper.settings import Settings

SERVICE = admin_pb2.DESCRIPTOR.services_by_name["Admin"]


class AdminProxy:
    """Forwards the calls of muru.admin.v1 that the allowlist admits."""

    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._channel: grpc.aio.Channel | None = None

    def channel(self) -> grpc.aio.Channel:
        """Return the channel to the admin socket, made on the worker's loop at first use."""

        if self._channel is None:
            # The authority a Unix socket's address gives is one the daemon
            # refuses (muruhq/muru#863; #33 here), so name a plain one. Messages are
            # not limited in size here: the daemon's own limits are the ones
            # that count.

            self._channel = grpc.aio.insecure_channel(
                f"unix:{self._settings.admin_socket}",
                options=[
                    ("grpc.default_authority", "localhost"),
                    ("grpc.max_receive_message_length", -1),
                    ("grpc.max_send_message_length", -1),
                ],
            )

        return self._channel

    async def _admit(self, method: str, request: bytes, context: Any) -> None:
        """End the call unless it carries the token and the allowlist admits it."""

        if not auth.authorised(context.invocation_metadata(), self._settings.token):
            await context.abort(grpc.StatusCode.UNAUTHENTICATED, auth.REFUSAL)

        why = allowlist.refusal(method, request)

        if why is not None:
            await context.abort(grpc.StatusCode.PERMISSION_DENIED, why)

    def _unary(self, method: str) -> Callable[[bytes, Any], Awaitable[bytes]]:
        """Make the handler of a call with one response."""

        path = f"/{SERVICE.full_name}/{method}"

        async def forward(request: bytes, context: Any) -> bytes:
            await self._admit(method, request, context)
            call: grpc.aio.UnaryUnaryMultiCallable[bytes, bytes] = self.channel().unary_unary(path)

            try:
                response = await call(request, timeout=context.time_remaining())
            except grpc.aio.AioRpcError as error:
                await context.abort(error.code(), error.details() or "")

            return response

        return forward

    def _stream(self, method: str) -> Callable[[bytes, Any], AsyncIterator[bytes]]:
        """Make the handler of a call whose responses stream."""

        path = f"/{SERVICE.full_name}/{method}"

        async def forward(request: bytes, context: Any) -> AsyncIterator[bytes]:
            await self._admit(method, request, context)
            method_call: grpc.aio.UnaryStreamMultiCallable[bytes, bytes] = (
                self.channel().unary_stream(path)
            )
            call = method_call(request, timeout=context.time_remaining())

            # The hub going away cancels this handler, which must end the
            # daemon's stream too, or a log tail would run on unread.

            try:
                async for response in call:
                    yield response
            except grpc.aio.AioRpcError as error:
                await context.abort(error.code(), error.details() or "")
            finally:
                call.cancel()

        return forward

    def handlers(self) -> grpc.GenericRpcHandler:
        """Return the handlers for every call of the service, refused ones included.

        A call the allowlist refuses still has a handler, so that it is
        answered PERMISSION_DENIED with the reason, not UNIMPLEMENTED.
        """

        handlers: dict[str, grpc.RpcMethodHandler[Any, Any]] = {}

        for method in SERVICE.methods:
            if method.client_streaming:
                continue

            if method.server_streaming:
                handlers[method.name] = grpc.unary_stream_rpc_method_handler(
                    self._stream(method.name)
                )
            else:
                handlers[method.name] = grpc.unary_unary_rpc_method_handler(
                    self._unary(method.name)
                )

        return grpc.method_handlers_generic_handler(SERVICE.full_name, handlers)
