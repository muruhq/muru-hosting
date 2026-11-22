"""Sites in the Django admin site, which local sign-in turns on."""

from django.contrib import admin

from hub.hosting.models import Deploy, Site


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin[Site]):
    """Sites as an admin lists and edits them."""

    list_display = ("name", "owner", "kind", "state", "created_at")
    list_filter = ("kind", "state")
    search_fields = ("name", "owner__username")


@admin.register(Deploy)
class DeployAdmin(admin.ModelAdmin[Deploy]):
    """Deploys as an admin lists them."""

    list_display = ("site", "release", "state", "description", "created_at")
    list_filter = ("state",)
