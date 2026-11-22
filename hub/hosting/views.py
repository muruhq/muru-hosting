"""The hub's pages for sites."""

from datetime import UTC, datetime

from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render

from hub.accounts.models import User
from hub.hosting import services
from hub.hosting.models import Deploy


def home(request: HttpRequest) -> HttpResponse:
    """Show the sites the signed-in person may see."""

    assert isinstance(request.user, User)

    return render(request, "hosting/home.html", {"sites": services.sites_visible_to(request.user)})


def site(request: HttpRequest, owner: str, name: str) -> HttpResponse:
    """Show one site: its state, its releases as its daemon has them, and the hub's deploys."""

    assert isinstance(request.user, User)

    # A site someone may not see is answered as one that does not exist.

    found = services.sites_visible_to(request.user).filter(owner__username=owner, name=name).first()

    if found is None:
        raise Http404("There is no such site.")

    live = services.live_site(found)
    deploys = list(found.deploys.all()[:20])
    by_release: dict[str, Deploy] = {deploy.release: deploy for deploy in deploys if deploy.release}

    releases = [
        {
            "id": release.id,
            "state": release.state,
            "serving": release.serving,
            "message": release.message,
            "created": datetime.fromtimestamp(release.created_unix_ms / 1000, tz=UTC),
            "deploy": by_release.get(release.id),
        }
        for release in live.releases
    ]

    return render(
        request,
        "hosting/site.html",
        {"site": found, "live": live, "releases": releases, "deploys": deploys},
    )
