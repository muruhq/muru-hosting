"""Sites in the Django admin site, which local sign-in turns on."""

from django.contrib import admin

from hub.hosting.models import Site


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin[Site]):
    """Sites as an admin lists and edits them."""

    list_display = ("name", "owner", "kind", "created_at")
    list_filter = ("kind",)
    search_fields = ("name", "owner__username")
