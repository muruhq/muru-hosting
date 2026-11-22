"""The hub's accounts."""

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """A person's account in the hub.

    The hub has a user model of its own from the first migration, so that
    what an account carries (its GitHub identity, its entitlements) can be
    added without replacing Django's. A superuser is a platform admin.
    """

    @property
    def is_platform_admin(self) -> bool:
        """Say whether the account may do everything in the hub."""

        return self.is_active and self.is_superuser
