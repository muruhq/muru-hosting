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
from hub.hosting import services
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


def _site_context(request: HttpRequest, found: Site) -> dict[str, Any]:
    """Gather what a site's page shows: the daemon's view of the site and the hub's own records."""

    assert isinstance(request.user, User)
    live = services.live_site(found)
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
            "time": _time(event.time_unix_ms),
            "type": event.type,
            "subject": event.subject,
            "level": event.level,
            "message": event.message,
        }
        for event in live.events
    ]

    return {
        "site": found,
        "live": live,
        "releases": releases,
        "deploys": deploys,
        "events": events,
        "log": "\n".join(live.log),
        "audit": list(found.audit_entries.select_related("actor")[:20]),
        "may_operate": services.may_operate(request.user, found),
        "deploy_from_disk": settings.HUB_DEPLOY_FROM_DISK,
        "busy": any(deploy.finished_at is None for deploy in deploys),
    }


def site(request: HttpRequest, owner: str, name: str) -> HttpResponse:
    """Show one site: its state, its releases, events and log, and what the hub did to it."""

    found = _visible_site(request, owner, name)

    return render(request, "hosting/site.html", _site_context(request, found))


def site_live(request: HttpRequest, owner: str, name: str) -> HttpResponse:
    """Return the part of a site's page that changes, for the page to refresh itself with."""

    found = _visible_site(request, owner, name)

    return render(request, "hosting/_site_live.html", _site_context(request, found))


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

        services.deploy_directory(found, Path(path).expanduser(), actor)

        return f"Queued a deploy of {path}."

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
