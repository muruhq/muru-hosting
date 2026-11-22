"""What every page is told about signing in."""

from django.conf import settings
from django.http import HttpRequest


def sign_in(request: HttpRequest) -> dict[str, bool]:
    """Tell templates whether the hub uses local accounts and has its admin site."""

    return {
        "local_sign_in": settings.HUB_SIGN_IN == settings.SIGN_IN_LOCAL,
        "admin_site": settings.HUB_ADMIN_SITE,
    }
