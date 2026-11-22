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
    def plan_deploy(
        self, source_path: str, env: dict[str, str], hold: bool = False
    ) -> admin_pb2.DeployPlan:
        """Ask the daemon what a deploy of a source would make, changing nothing."""

        try:
            plan: admin_pb2.DeployPlan = self._admin.PlanDeploy(
                self._deploy_request(source_path, env, hold),
                metadata=self._metadata,
                timeout=TIMEOUT,
            )
        except grpc.RpcError as error:
            raise HelperError("planning the deploy", error) from error

        return plan

    @observed(label="helper.deploy", category="external", capture="none")
    def deploy(
        self, source_path: str, env: dict[str, str], release: str, hold: bool = False
    ) -> admin_pb2.Release:
        """Create a release from a source, with the id given, without waiting for it.

        With `hold` the release is started and traffic is left where it is.
        """

        request = self._deploy_request(source_path, env, hold)
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

    @observed(label="helper.app", category="external", capture="none")
    def app(self) -> admin_pb2.App | None:
        """Return the site's application as the daemon has it, or None before its first release."""

        try:
            found: admin_pb2.App = self._admin.GetApp(
                admin_pb2.GetAppRequest(name=APP), metadata=self._metadata, timeout=TIMEOUT
            )
        except grpc.RpcError as error:
            if error.code() == grpc.StatusCode.NOT_FOUND:
                return None

            raise HelperError("reading the site's application", error) from error

        return found

    @observed(label="helper.rollback", category="external", capture="none")
    def rollback(self) -> admin_pb2.Release:
        """Move traffic back to the release that served before, and return it."""

        try:
            restored: admin_pb2.Release = self._admin.Rollback(
                admin_pb2.RollbackRequest(app=APP), metadata=self._metadata, timeout=TIMEOUT
            )
        except grpc.RpcError as error:
            raise HelperError("rolling back", error) from error

        return restored

    @observed(label="helper.promote", category="external", capture="none")
    def promote(self, release: str) -> admin_pb2.Release:
        """Move traffic to a release now, and return it."""

        try:
            promoted: admin_pb2.Release = self._admin.PromoteRelease(
                admin_pb2.PromoteReleaseRequest(app=APP, release=release),
                metadata=self._metadata,
                timeout=TIMEOUT,
            )
        except grpc.RpcError as error:
            raise HelperError("promoting the release", error) from error

        return promoted

    @observed(label="helper.restart_worker", category="external", capture="none")
    def restart_worker(self, release: str, group: str, index: int) -> admin_pb2.WorkerDebug:
        """Replace one worker of a release with a fresh one, and return what it answered.

        The call returns once the replacement is started, before it serves.
        """

        try:
            response = self._admin.Debug(
                admin_pb2.DebugRequest(
                    app=APP, release=release, op="restart", group=group, worker=index
                ),
                metadata=self._metadata,
                timeout=TIMEOUT,
            )
        except grpc.RpcError as error:
            raise HelperError("restarting a worker", error) from error

        answer: admin_pb2.WorkerDebug = response.workers[0]

        return answer

    @observed(label="helper.set_maintenance", category="external", capture="none")
    def set_maintenance(self, on: bool) -> admin_pb2.MaintenanceStatus:
        """Turn the site's maintenance page on or off."""

        try:
            status: admin_pb2.MaintenanceStatus = self._admin.SetMaintenance(
                admin_pb2.SetMaintenanceRequest(app=APP, on=on),
                metadata=self._metadata,
                timeout=TIMEOUT,
            )
        except grpc.RpcError as error:
            raise HelperError("setting maintenance", error) from error

        return status

    @observed(label="helper.events", category="external", capture="none")
    def events(self, newest: int) -> list[admin_pb2.Event]:
        """Return the daemon's most recent events, newest first.

        The call lists events from the oldest kept and cannot be asked for
        the newest alone, so every kept event is read to return the last few
        (muruhq/muru#870; #38 here).
        """

        try:
            response = self._admin.ListEvents(
                admin_pb2.ListEventsRequest(), metadata=self._metadata, timeout=TIMEOUT
            )
        except grpc.RpcError as error:
            raise HelperError("listing the site's events", error) from error

        return list(response.events)[-newest:][::-1]

    @observed(label="helper.log", category="external", capture="none")
    def log(self, lines: int) -> list[str]:
        """Return the last lines of the serving release's log, oldest first."""

        try:
            tail = self._admin.TailLogs(
                admin_pb2.TailLogsRequest(app=APP, lines=lines),
                metadata=self._metadata,
                timeout=TIMEOUT,
            )

            return [entry.line for entry in tail]
        except grpc.RpcError as error:
            raise HelperError("reading the site's log", error) from error

    @observed(label="helper.rollout", category="external", capture="none")
    def rollout(self) -> admin_pb2.Rollout | None:
        """Return the site's latest rollout, under way or ended, or None when it has had none."""

        try:
            found: admin_pb2.Rollout = self._admin.GetRollout(
                admin_pb2.GetRolloutRequest(app=APP), metadata=self._metadata, timeout=TIMEOUT
            )
        except grpc.RpcError as error:
            if error.code() == grpc.StatusCode.NOT_FOUND:
                return None

            raise HelperError("reading the site's rollout", error) from error

        return found

    @observed(label="helper.start_rollout", category="external", capture="none")
    def start_rollout(
        self, release: str, steps: list[int], hold_seconds: int, min_requests: int
    ) -> admin_pb2.Rollout:
        """Start a canary of a held release: each step's share of requests, each for the hold."""

        try:
            started: admin_pb2.Rollout = self._admin.StartRollout(
                admin_pb2.StartRolloutRequest(
                    app=APP,
                    release=release,
                    steps=[
                        admin_pb2.RolloutStep(percent=percent, hold_ms=hold_seconds * 1000)
                        for percent in steps
                    ],
                    min_requests=min_requests,
                ),
                metadata=self._metadata,
                timeout=TIMEOUT,
            )
        except grpc.RpcError as error:
            raise HelperError("starting the rollout", error) from error

        return started

    @observed(label="helper.control_rollout", category="external", capture="none")
    def control_rollout(self, action: str) -> admin_pb2.Rollout:
        """Pause, resume, promote or abort the site's rollout, and return it as it then is."""

        calls = {
            "pause": self._admin.PauseRollout,
            "resume": self._admin.ResumeRollout,
            "promote": self._admin.PromoteRollout,
            "abort": self._admin.AbortRollout,
        }

        try:
            rollout: admin_pb2.Rollout = calls[action](
                admin_pb2.RolloutControlRequest(app=APP), metadata=self._metadata, timeout=TIMEOUT
            )
        except grpc.RpcError as error:
            raise HelperError(f"asking the rollout to {action}", error) from error

        return rollout

    @observed(label="helper.commands", category="external", capture="none")
    def commands(self) -> list[admin_pb2.CommandInfo]:
        """List the commands the serving release declares."""

        try:
            response = self._admin.ListCommands(
                admin_pb2.ListCommandsRequest(app=APP), metadata=self._metadata, timeout=TIMEOUT
            )
        except grpc.RpcError as error:
            if error.code() == grpc.StatusCode.NOT_FOUND:
                return []

            raise HelperError("listing the site's commands", error) from error

        return list(response.commands)

    @observed(label="helper.run_command", category="external", capture="none")
    def run_command(self, name: str, inputs: dict[str, str]) -> int:
        """Start a declared command, detached from this call, and return its run's id."""

        try:
            output = self._admin.RunCommand(
                admin_pb2.RunCommandRequest(app=APP, name=name, inputs=inputs, detach=True),
                metadata=self._metadata,
                timeout=TIMEOUT,
            )
            run = next((message.run for message in output if message.run), 0)
        except grpc.RpcError as error:
            raise HelperError(f"running {name}", error) from error

        return run

    @observed(label="helper.command_runs", category="external", capture="none")
    def command_runs(self) -> list[admin_pb2.CommandRunRecord]:
        """List the runs of the site's commands that the daemon keeps, those under way first."""

        try:
            response = self._admin.ListCommandRuns(
                admin_pb2.ListCommandRunsRequest(app=APP), metadata=self._metadata, timeout=TIMEOUT
            )
        except grpc.RpcError as error:
            raise HelperError("listing the site's command runs", error) from error

        return list(response.runs)

    @observed(label="helper.command_run", category="external", capture="none")
    def command_run(self, run: int) -> admin_pb2.CommandRunRecord | None:
        """Return one run of a command, or None when the daemon keeps none by that id."""

        try:
            record: admin_pb2.CommandRunRecord = self._admin.GetCommandRun(
                admin_pb2.GetCommandRunRequest(run=run), metadata=self._metadata, timeout=TIMEOUT
            )
        except grpc.RpcError as error:
            if error.code() == grpc.StatusCode.NOT_FOUND:
                return None

            raise HelperError("reading the command run", error) from error

        return record

    @observed(label="helper.command_output", category="external", capture="none")
    def command_output(self, run: int, lines: int) -> list[str]:
        """Return the last lines a run of a command has written, oldest first."""

        try:
            tail = self._admin.TailCommandRun(
                admin_pb2.TailCommandRunRequest(run=run, lines=lines),
                metadata=self._metadata,
                timeout=TIMEOUT,
            )

            return [entry.line for entry in tail]
        except grpc.RpcError as error:
            raise HelperError("reading the command's output", error) from error

    @observed(label="helper.stop_command_run", category="external", capture="none")
    def stop_command_run(self, run: int) -> admin_pb2.CommandRunRecord:
        """Stop a run that is under way, as its timeout would."""

        try:
            record: admin_pb2.CommandRunRecord = self._admin.StopCommandRun(
                admin_pb2.StopCommandRunRequest(run=run), metadata=self._metadata, timeout=TIMEOUT
            )
        except grpc.RpcError as error:
            raise HelperError("stopping the command", error) from error

        return record

    def _deploy_request(
        self, source_path: str, env: dict[str, str], hold: bool = False
    ) -> admin_pb2.DeployRequest:
        # Each release takes its settings from its own source and from the
        # hub alone. Without `fresh`, Muru fills what they leave out from
        # the release before, which for a site's first deploy is the hello
        # site, its static directory included (muruhq/muru#861; #31 here).

        return admin_pb2.DeployRequest(
            app=APP,
            source=source_path,
            fresh=True,
            hold=hold,
            env=[admin_pb2.EnvEntry(name=name, value=value) for name, value in sorted(env.items())],
        )
