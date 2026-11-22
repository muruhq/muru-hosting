"""The hub's URLs."""

from django.conf import settings
from django.contrib import admin
from django.contrib.auth.decorators import login_not_required
from django.contrib.staticfiles import views as staticfiles_views
from django.urls import URLPattern, URLResolver, include, path, re_path

urlpatterns: list[URLPattern | URLResolver] = [
    path("", include("hub.accounts.urls")),
    path("", include("hub.hosting.urls")),
]

# The Django admin site is how local accounts are made, and is off otherwise.

if settings.HUB_ADMIN_SITE:
    urlpatterns.append(path("admin/", admin.site.urls))

# A development run serves static files from each application, to someone
# not signed in too, since the sign-in page has a stylesheet.

if settings.DEBUG:
    urlpatterns.append(
        re_path(
            rf"^{settings.STATIC_URL.strip('/')}/(?P<path>.*)$",
            login_not_required(staticfiles_views.serve),
        )
    )
