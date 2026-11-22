"""Fixtures and markers shared by the hub's tests."""

import pytest
from django.db import connection

from hub.accounts.models import User


def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    """Skip the tests that need Postgres when the suite runs on another database."""

    if connection.vendor == "postgresql":
        return

    skip = pytest.mark.skip(reason="needs Postgres: set DATABASE_URL to one")

    for item in items:
        if "postgres" in item.keywords:
            item.add_marker(skip)


@pytest.fixture
def member(db: None) -> User:
    """Make an ordinary account."""

    return User.objects.create_user("alice", password="correct horse")


@pytest.fixture
def admin(db: None) -> User:
    """Make a platform admin."""

    return User.objects.create_superuser("root", password="battery staple")
