"""The helper's entry point: what Muru calls to register its gRPC services."""

from __future__ import annotations

from typing import Any

from muruhosting_stubs.muruhosting.site.v1 import sources_pb2_grpc

from muruhosting_helper import settings as helper_settings
from muruhosting_helper.proxy import AdminProxy
from muruhosting_helper.sources import SourcesServicer


def register(server: Any) -> None:
    """Register the admin API's proxy and the Sources service on Muru's gRPC server.

    There is no health service here: Muru's edge answers `grpc.health.v1`
    for a release itself, and a release cannot add to its answer
    (muruhq/muru#864). The hub asks the proxied `GetStatus` instead, which
    answers only while the admin socket does.
    """

    settings = helper_settings.load()
    settings.sources_dir.mkdir(parents=True, exist_ok=True)

    server.add_generic_rpc_handlers((AdminProxy(settings).handlers(),))
    sources_pb2_grpc.add_SourcesServicer_to_server(SourcesServicer(settings), server)
