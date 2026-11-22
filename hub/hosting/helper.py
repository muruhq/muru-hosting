"""The hub's client for a site's helper.

Everything the hub does to a site's daemon goes through here: the calls of
muru.admin.v1 that the helper proxies, and its own Sources service
(specification section 4). When Muru's admin listener replaces the helper,
only the Sources calls and the address change.
"""

from __future__ import annotations

from collections.abc import Iterator
from types import TracebackType
from typing import Self

import grpc
from muruhosting_stubs.muru.admin.v1 import admin_pb2, admin_pb2_grpc
from muruhosting_stubs.muruhosting.site.v1 import sources_pb2, sources_pb2_grpc

from hub.hosting.models import APP
from hub.tracing import observed

CHUNK = 256 * 1024

# How long a call that only reads or records may take. Calls that wait for
# a release say how long themselves.

TIMEOUT = 15.0


class HelperError(Exception):
    """A call to a site's helper that failed, with what the helper or the daemon said."""

    def __init__(self, action: str, error: grpc.RpcError) -> None:
        self.code: grpc.StatusCode = error.code()
        self.details: str = error.details() or ""
        super().__init__(f"{action}: {self.details or self.code.name}")

    @property
    def unreachable(self) -> bool:
        """Say whether the helper, or the daemon behind it, did not answer at all."""

        return self.code in {grpc.StatusCode.UNAVAILABLE, grpc.StatusCode.DEADLINE_EXCEEDED}


class HelperClient:
    """Calls to one site's helper, each carrying the site's token."""

    def __init__(self, address: str, token: str) -> None:
        self.address = address
        self._metadata = (("authorization", f"Bearer {token}"),)

        # A local site's helper listens on loopback without TLS (specification
        # section 15.3).

        self._channel = grpc.insecure_channel(address)
        self._admin = admin_pb2_grpc.AdminStub(self._channel)
        self._sources = sources_pb2_grpc.SourcesStub(self._channel)

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        kind: type[BaseException] | None,
        error: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self.close()

    def close(self) -> None:
        """Close the connection to the helper."""

        self._channel.close()

    @observed(label="helper.status", category="external", capture="none")
    def status(self) -> admin_pb2.Status:
        """Ask the daemon for its status, which also says that it is up."""

        try:
            status: admin_pb2.Status = self._admin.GetStatus(
                admin_pb2.GetStatusRequest(), metadata=self._metadata, timeout=TIMEOUT
            )
        except grpc.RpcError as error:
            raise HelperError("asking the site's daemon for its status", error) from error

        return status

    @observed(label="helper.apply_config", category="external", capture="none")
    def apply_config(self, document: str) -> admin_pb2.ConfigReport:
        """Apply a declarative document to the daemon, adding to what it has."""

        try:
            report: admin_pb2.ConfigReport = self._admin.ApplyConfig(
                admin_pb2.ApplyConfigRequest(document=document),
                metadata=self._metadata,
                timeout=TIMEOUT,
            )
        except grpc.RpcError as error:
            raise HelperError("applying the site's configuration", error) from error

        return report

    @observed(label="helper.upload_source", category="external", capture="none")
    def upload_source(self, name: str, sha256: str, commit: str, archive: bytes) -> str:
        """Upload a source archive, and return its directory as the daemon reads it."""

        def messages() -> Iterator[sources_pb2.UploadSourceRequest]:
            yield sources_pb2.UploadSourceRequest(
                header=sources_pb2.UploadSourceHeader(name=name, sha256=sha256, commit=commit)
            )

            for start in range(0, len(archive), CHUNK):
                yield sources_pb2.UploadSourceRequest(chunk=archive[start : start + CHUNK])

        try:
            source = self._sources.UploadSource(messages(), metadata=self._metadata, timeout=300)
        except grpc.RpcError as error:
            raise HelperError("uploading the source", error) from error

        return str(source.path)

    @observed(label="helper.plan_deploy", category="external", capture="none")
    def plan_deploy(self, source_path: str, env: dict[str, str]) -> admin_pb2.DeployPlan:
        """Ask the daemon what a deploy of a source would make, changing nothing."""

        try:
            plan: admin_pb2.DeployPlan = self._admin.PlanDeploy(
                self._deploy_request(source_path, env), metadata=self._metadata, timeout=TIMEOUT
            )
        except grpc.RpcError as error:
            raise HelperError("planning the deploy", error) from error

        return plan

    @observed(label="helper.deploy", category="external", capture="none")
    def deploy(self, source_path: str, env: dict[str, str], release: str) -> admin_pb2.Release:
        """Create a release from a source, with the id given, without waiting for it."""

        request = self._deploy_request(source_path, env)
        request.release = release

        try:
            made: admin_pb2.Release = self._admin.Deploy(
                request, metadata=self._metadata, timeout=TIMEOUT
            )
        except grpc.RpcError as error:
            raise HelperError("deploying the release", error) from error

        return made

    @observed(label="helper.release", category="external", capture="none")
    def release(self, release: str) -> admin_pb2.Release | None:
        """Return a release of the site, or None when the daemon has none by that id."""

        try:
            found: admin_pb2.Release = self._admin.GetRelease(
                admin_pb2.GetReleaseRequest(app=APP, release=release),
                metadata=self._metadata,
                timeout=TIMEOUT,
            )
        except grpc.RpcError as error:
            if error.code() == grpc.StatusCode.NOT_FOUND:
                return None

            raise HelperError("reading the release", error) from error

        return found

    @observed(label="helper.wait_release", category="external", capture="none")
    def wait_release(self, release: str, timeout: float) -> admin_pb2.Release:
        """Wait until a release is ready or has failed, and return it as it then is."""

        try:
            settled: admin_pb2.Release = self._admin.WaitRelease(
                admin_pb2.WaitReleaseRequest(
                    app=APP, release=release, timeout_ms=int(timeout * 1000)
                ),
                metadata=self._metadata,
                timeout=timeout + TIMEOUT,
            )
        except grpc.RpcError as error:
            raise HelperError("waiting for the release", error) from error

        return settled

    @observed(label="helper.releases", category="external", capture="none")
    def releases(self) -> list[admin_pb2.Release]:
        """List the site's releases, as the daemon has them."""

        try:
            response = self._admin.ListReleases(
                admin_pb2.ListReleasesRequest(app=APP), metadata=self._metadata, timeout=TIMEOUT
            )
        except grpc.RpcError as error:
            raise HelperError("listing the site's releases", error) from error

        return list(response.releases)

    def _deploy_request(self, source_path: str, env: dict[str, str]) -> admin_pb2.DeployRequest:
        # Each release takes its settings from its own source and from the
        # hub alone. Without `fresh`, Muru fills what they leave out from
        # the release before, which for a site's first deploy is the hello
        # site, its static directory included (muruhq/muru#861).

        return admin_pb2.DeployRequest(
            app=APP,
            source=source_path,
            fresh=True,
            env=[admin_pb2.EnvEntry(name=name, value=value) for name, value in sorted(env.items())],
        )
