"""The hub's pages for sites."""

from collections.abc import Callable
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from django.conf import settings
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from hub.accounts.models import User
from hub.hosting import live, services
from hub.hosting.models import Deploy, Site

# The states of a release that traffic can be moved to: started and held,
# or kept warm after it stopped serving.

PROMOTABLE = frozenset({"ready", "retained"})


def home(request: HttpRequest) -> HttpResponse:
    """Show the sites the signed-in person may see."""

    assert isinstance(request.user, User)

    return render(request, "hosting/home.html", {"sites": services.sites_visible_to(request.user)})


def _visible_site(request: HttpRequest, owner: str, name: str) -> Site:
    """Find a site the signed-in person may see.

    A site someone may not see is answered as one that does not exist.
    """

    assert isinstance(request.user, User)
    found = services.sites_visible_to(request.user).filter(owner__username=owner, name=name).first()

    if found is None:
        raise Http404("There is no such site.")

    return found


def _time(unix_ms: int) -> datetime:
    return datetime.fromtimestamp(unix_ms / 1000, tz=UTC)


def _site_context(request: HttpRequest, found: Site, feed: bool = True) -> dict[str, Any]:
    """Gather what a site's page shows: the daemon's view of the site and the hub's own records.

    `feed` says whether the log and the events are wanted, which they are
    for the whole page and not for the part of it that refreshes.
    """

    assert isinstance(request.user, User)
    live = services.live_site(found, feed=feed)
    deploys = list(found.deploys.all()[:20])
    by_release: dict[str, Deploy] = {deploy.release: deploy for deploy in deploys if deploy.release}

    releases = [
        {
            "id": release.id,
            "state": release.state,
            "serving": release.serving,
            "message": release.message,
            "created": _time(release.created_unix_ms),
            "deploy": by_release.get(release.id),
            "promotable": not release.serving and release.state in PROMOTABLE,
        }
        for release in live.releases
    ]

    events = [
        {
            "sequence": event.sequence,
            "time": _time(event.time_unix_ms),
            "type": event.type,
            "subject": event.subject,
            "level": event.level,
            "message": event.message,
        }
        for event in live.events
    ]

    runs = [
        {
            "id": run.run,
            "name": run.name,
            "release": run.release,
            "inputs": run.inputs,
            "started": _time(run.started_unix_ms),
            "under_way": run.under_way,
            "ok": run.ok,
            "message": run.message,
        }
        for run in live.command_runs
    ]

    return {
        "site": found,
        "live": live,
        "rollout": _rollout_context(live.rollout),
        "runs": runs,
        "releases": releases,
        "deploys": deploys,
        "events": events,
        "log": "\n".join(live.log),
        "audit": list(found.audit_entries.select_related("actor")[:20]),
        "may_operate": services.may_operate(request.user, found),
        "deploy_from_disk": settings.HUB_DEPLOY_FROM_DISK,
        "busy": any(deploy.finished_at is None for deploy in deploys),
    }


# The states of a rollout that is still under way, and so can be controlled.

ROLLOUT_UNDER_WAY = frozenset({"running", "paused", "awaiting_approval"})

ROLLOUT_STATES = {
    "running": "Running",
    "paused": "Paused",
    "awaiting_approval": "Waiting for approval",
    "promoted": "Promoted",
    "rolled_back": "Rolled back",
}


def _rollout_context(rollout: Any) -> dict[str, Any] | None:
    """Describe a site's latest rollout as its page shows it."""

    if rollout is None:
        return None

    return {
        "id": rollout.id,
        "candidate": rollout.candidate,
        "baseline": rollout.baseline,
        "state": rollout.state,
        "state_label": ROLLOUT_STATES.get(rollout.state, rollout.state),
        "under_way": rollout.state in ROLLOUT_UNDER_WAY,
        "paused": rollout.state in {"paused", "awaiting_approval"},
        "percent": rollout.percent,
        "step": rollout.step + 1,
        "steps": [step.percent for step in rollout.steps],
        "message": rollout.message,
        "updated": _time(rollout.updated_unix_ms),
    }


def site(request: HttpRequest, owner: str, name: str) -> HttpResponse:
    """Show one site: its state, its releases, events and log, and what the hub did to it."""

    found = _visible_site(request, owner, name)

    return render(request, "hosting/site.html", _site_context(request, found))


def site_live(request: HttpRequest, owner: str, name: str) -> HttpResponse:
    """Return the part of a site's page that changes, for the page to refresh itself with."""

    found = _visible_site(request, owner, name)

    return render(request, "hosting/_site_live.html", _site_context(request, found, feed=False))


def site_stream(request: HttpRequest, owner: str, name: str) -> HttpResponse:
    """Stream a site's log and events to its page for as long as the page is open.

    The request is handed to an ASGI application on the worker's event loop
    (Muru's handoff), so the stream holds none of the worker's threads.
    Where the hub is not served by Muru, or the handoff is not enabled, the
    answer is 501 and the page shows the log and events it was loaded with.
    """

    found = _visible_site(request, owner, name)
    bridge = request.META.get("muru.wsgi_to_asgi")

    if bridge is None or not found.helper_address:
        return HttpResponse("This hub cannot stream.\n", status=501, content_type="text/plain")

    bridge.scope["state"]["helper_address"] = found.helper_address
    bridge.scope["state"]["helper_token"] = found.helper_token

    try:
        bridge.handoff(live.site_stream)
    except RuntimeError:
        return HttpResponse("This hub cannot stream.\n", status=501, content_type="text/plain")

    return HttpResponse()


def _act(
    request: HttpRequest, owner: str, name: str, action: Callable[[Site, User], str]
) -> HttpResponse:
    """Take an action on a site for the signed-in person, then show the site again.

    What came of it, or why it was refused, is shown at the top of the page.
    """

    found = _visible_site(request, owner, name)
    assert isinstance(request.user, User)

    if not services.may_operate(request.user, found):
        raise PermissionDenied("You may look at this site but not change it.")

    try:
        messages.success(request, action(found, request.user))
    except services.ActionRefused as refused:
        messages.error(request, str(refused))

    return redirect("site", owner, name)


@require_POST
def deploy(request: HttpRequest, owner: str, name: str) -> HttpResponse:
    """Deploy a directory of the hub's machine, or the hello site again."""

    def action(found: Site, actor: User) -> str:
        if request.POST.get("source") == "hello":
            services.redeploy_hello(found, actor)

            return "Queued a deploy of the hello site."

        path = request.POST.get("path", "").strip()

        if not path:
            raise services.ActionRefused("Give the directory to deploy.")

        hold = request.POST.get("hold") == "1"
        services.deploy_directory(found, Path(path).expanduser(), actor, hold=hold)

        return f"Queued a deploy of {path}{', to be held' if hold else ''}."

    return _act(request, owner, name, action)


@require_POST
def roll_back(request: HttpRequest, owner: str, name: str) -> HttpResponse:
    """Move traffic back to the release that served before."""

    return _act(request, owner, name, services.roll_back)


@require_POST
def promote(request: HttpRequest, owner: str, name: str, release: str) -> HttpResponse:
    """Move traffic to one release."""

    return _act(request, owner, name, lambda found, actor: services.promote(found, release, actor))


@require_POST
def restart(request: HttpRequest, owner: str, name: str) -> HttpResponse:
    """Restart the serving release's workers."""

    return _act(request, owner, name, services.restart)


@require_POST
def maintenance(request: HttpRequest, owner: str, name: str) -> HttpResponse:
    """Turn the maintenance page on or off."""

    on = request.POST.get("on") == "1"

    return _act(
        request, owner, name, lambda found, actor: services.set_maintenance(found, on, actor)
    )


def _operable_site(request: HttpRequest, owner: str, name: str) -> Site:
    """Find a site the signed-in person may act on, for a page that only they are shown."""

    found = _visible_site(request, owner, name)
    assert isinstance(request.user, User)

    if not services.may_operate(request.user, found):
        raise PermissionDenied("You may look at this site but not change it.")

    return found


def _number(request: HttpRequest, field: str, default: int) -> int:
    """Read a whole number from a form, or refuse saying which field was not one."""

    try:
        return int(request.POST.get(field, "") or default)
    except ValueError:
        raise services.ActionRefused(f"Give {field.replace('_', ' ')} as a whole number.") from None


def canary(request: HttpRequest, owner: str, name: str, release: str) -> HttpResponse:
    """Ask how a canary of a held release should go, and start it."""

    found = _operable_site(request, owner, name)
    assert isinstance(request.user, User)
    form = {"steps": "10,50", "hold": "60", "min_requests": "20"}

    if request.method == "POST":
        form = {key: request.POST.get(key, "") for key in form}

        try:
            message = services.start_rollout(
                found,
                release,
                form["steps"],
                _number(request, "hold", 60),
                _number(request, "min_requests", 20),
                request.user,
            )
        except services.ActionRefused as refused:
            messages.error(request, str(refused))
        else:
            messages.success(request, message)

            return redirect("site", owner, name)

    return render(request, "hosting/canary.html", {"site": found, "release": release, "form": form})


@require_POST
def rollout(request: HttpRequest, owner: str, name: str, action: str) -> HttpResponse:
    """Pause, resume, promote or abort the site's rollout."""

    return _act(
        request, owner, name, lambda found, actor: services.control_rollout(found, action, actor)
    )


def command(request: HttpRequest, owner: str, name: str, command: str) -> HttpResponse:
    """Show a declared command with its inputs, and run it."""

    found = _operable_site(request, owner, name)
    assert isinstance(request.user, User)
    declared = next(
        (item for item in services.live_site(found, feed=False).commands if item.name == command),
        None,
    )

    if declared is None:
        raise Http404("The serving release declares no such command.")

    if request.method == "POST":
        inputs = {item.name: request.POST.get(f"input-{item.name}", "") for item in declared.inputs}

        try:
            run = services.run_command(found, command, inputs, request.user)
        except services.ActionRefused as refused:
            messages.error(request, str(refused))
        else:
            return redirect("site-run", owner, name, run)

    return render(request, "hosting/command.html", {"site": found, "command": declared})


def run(request: HttpRequest, owner: str, name: str, run: int) -> HttpResponse:
    """Show one run of a site's command: how it stands and what it has written."""

    found = _visible_site(request, owner, name)
    assert isinstance(request.user, User)

    try:
        shown = services.command_run(found, run)
    except services.ActionRefused as refused:
        messages.error(request, str(refused))
        shown = None

    if shown is None:
        raise Http404("The site has no such run.")

    record = shown.record

    return render(
        request,
        "hosting/run.html",
        {
            "site": found,
            "run": record,
            "started": _time(record.started_unix_ms),
            "output": "\n".join(shown.output),
            "may_operate": services.may_operate(request.user, found),
        },
    )


def run_stream(request: HttpRequest, owner: str, name: str, run: int) -> HttpResponse:
    """Stream a run's output to its page until the run ends, as `site_stream` does a site's log."""

    found = _visible_site(request, owner, name)
    bridge = request.META.get("muru.wsgi_to_asgi")

    # The run must be this site's before its output is sent anywhere.

    try:
        shown = services.command_run(found, run)
    except services.ActionRefused:
        shown = None

    if shown is None:
        raise Http404("The site has no such run.")

    if bridge is None:
        return HttpResponse("This hub cannot stream.\n", status=501, content_type="text/plain")

    bridge.scope["state"]["helper_address"] = found.helper_address
    bridge.scope["state"]["helper_token"] = found.helper_token
    bridge.scope["state"]["run"] = run

    try:
        bridge.handoff(live.run_stream)
    except RuntimeError:
        return HttpResponse("This hub cannot stream.\n", status=501, content_type="text/plain")

    return HttpResponse()


@require_POST
def run_stop(request: HttpRequest, owner: str, name: str, run: int) -> HttpResponse:
    """Stop a run that is under way, then show the run again."""

    found = _operable_site(request, owner, name)
    assert isinstance(request.user, User)

    try:
        messages.success(request, services.stop_command_run(found, run, request.user))
    except services.ActionRefused as refused:
        messages.error(request, str(refused))

    return redirect("site-run", owner, name, run)
