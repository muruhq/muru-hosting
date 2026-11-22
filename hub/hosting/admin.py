"""Sites in the Django admin site, which local sign-in turns on."""

from django.contrib import admin

from hub.hosting.models import AuditEntry, Deploy, Site


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


@admin.register(AuditEntry)
class AuditEntryAdmin(admin.ModelAdmin[AuditEntry]):
    """The audit log as an admin reads it."""

    list_display = ("created_at", "site", "actor", "action", "detail", "succeeded")
    list_filter = ("action", "succeeded", "via")
