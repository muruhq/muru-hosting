"""Signing in and out."""

from typing import Any

from django.conf import settings
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_not_required
from django.http import HttpRequest
from django.http.response import HttpResponseBase
from django.shortcuts import render
from django.utils.decorators import method_decorator


@method_decorator(login_not_required, name="dispatch")
class SignInView(auth_views.LoginView):
    """The sign-in page, for the way of signing in the hub is set to use."""

    template_name = "registration/login.html"
    redirect_authenticated_user = True

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponseBase:
        """Take a username and password with local sign-in, and say why not otherwise."""

        # Signing in with GitHub needs the GitHub App, which this hub does
        # not have: say so instead of offering a form that cannot work.

        if settings.HUB_SIGN_IN != settings.SIGN_IN_LOCAL:
            return render(request, "registration/unavailable.html", status=503)

        return super().dispatch(request, *args, **kwargs)
