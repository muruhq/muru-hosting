"""The hub's pages for sites."""

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from hub.accounts.models import User
from hub.hosting import services


def home(request: HttpRequest) -> HttpResponse:
    """Show the sites the signed-in person may see."""

    assert isinstance(request.user, User)

    return render(request, "hosting/home.html", {"sites": services.sites_visible_to(request.user)})
