"""Which calls of muru.admin.v1 the hub may ever make through the helper.

Specification section 4.2. This is what the hub may do at all; which person
may do what is the hub's own check. A call not named here is refused, so a
call a new Muru release adds stays refused until it is listed.
"""

from __future__ import annotations

from muruhosting_stubs.muru.admin.v1 import admin_pb2

READING = frozenset(
    {
        "GetStatus",
        "Probe",
        "ListProcesses",
        "ListApps",
        "GetApp",
        "GetAppData",
        "ListReleases",
        "GetRelease",
        "WaitRelease",
        "ListRollouts",
        "GetRollout",
        "GetScaleStatus",
        "ApplicationUrls",
        "ListEvents",
        "WatchEvents",
        "ListHosts",
        "ListRoutes",
        "ListUpstreams",
        "DiffConfig",
        "ExportConfig",
        "TailLogs",
        "ListLogs",
        "GetMetrics",
        "ListWebSockets",
        "ListOverlays",
        "PreviewOverlay",
        "ListCommands",
        "ListCommandRuns",
        "GetCommandRun",
        "TailCommandRun",
        "ListConditions",
    }
)

CHANGING = frozenset(
    {
        "PlanDeploy",
        "Deploy",
        "Rollback",
        "DrainRelease",
        "PromoteRelease",
        "PruneReleases",
        "RemoveRelease",
        "StartRollout",
        "PauseRollout",
        "ResumeRollout",
        "PromoteRollout",
        "AbortRollout",
        "SetScale",
        "SetMaintenance",
        "ControlOverlay",
        "ApplyConfig",
        "RunCommand",
        "StopCommandRun",
        "Debug",
    }
)

ALLOWED = READING | CHANGING

# The debug operations that look at, or restart, workers. The others run
# code in a worker (inspect) or dump its memory.

DEBUG_OPERATIONS = frozenset({"status", "stacks", "tasks", "restart"})


def refusal(method: str, request: bytes) -> str | None:
    """Say why a call is refused, or None when the hub may make it.

    `method` is the call's name, such as `Deploy`, and `request` its request
    message as it arrived.
    """

    if method not in ALLOWED:
        return f"{method} is not a call the hub may make"

    # Only a command the release declares, never one-off code.

    if method == "RunCommand":
        run = admin_pb2.RunCommandRequest.FromString(request)

        if run.argv or not run.name:
            return "RunCommand is allowed for a declared command only, by name"

    if method == "Debug":
        debug = admin_pb2.DebugRequest.FromString(request)

        if debug.op not in DEBUG_OPERATIONS:
            return f"Debug is allowed for {', '.join(sorted(DEBUG_OPERATIONS))} only"

    return None
