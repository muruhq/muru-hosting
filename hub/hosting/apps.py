"""The hosting application's configuration."""

from django.apps import AppConfig


class HostingConfig(AppConfig):
    """Hosting: the sites the hub manages."""

    name = "hub.hosting"
    label = "hosting"
