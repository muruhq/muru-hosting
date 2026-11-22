"""URLs for the hub's site pages."""

from django.urls import path

from hub.hosting import views

urlpatterns = [
    path("", views.home, name="home"),
    path("sites/<str:owner>/<str:name>/", views.site, name="site"),
]
