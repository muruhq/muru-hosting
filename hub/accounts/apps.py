"""The accounts application's configuration."""

from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """Accounts: who signs in to the hub, and how."""

    name = "hub.accounts"
    label = "accounts"
