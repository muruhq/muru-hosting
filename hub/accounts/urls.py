"""URLs for signing in and out."""

from django.contrib.auth import views as auth_views
from django.urls import path

from hub.accounts import views

urlpatterns = [
    path("sign-in/", views.SignInView.as_view(), name="sign-in"),
    path("sign-out/", auth_views.LogoutView.as_view(), name="sign-out"),
]
