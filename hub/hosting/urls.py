"""URLs for the hub's site pages."""

from django.urls import path

from hub.hosting import views

SITE = "sites/<str:owner>/<str:name>/"

urlpatterns = [
    path("", views.home, name="home"),
    path(SITE, views.site, name="site"),
    path(f"{SITE}live/", views.site_live, name="site-live"),
    path(f"{SITE}deploy/", views.deploy, name="site-deploy"),
    path(f"{SITE}roll-back/", views.roll_back, name="site-roll-back"),
    path(f"{SITE}restart/", views.restart, name="site-restart"),
    path(f"{SITE}maintenance/", views.maintenance, name="site-maintenance"),
    path(f"{SITE}releases/<str:release>/promote/", views.promote, name="site-promote"),
]
