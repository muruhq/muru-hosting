"""Settings for the test suite: the hub's own, as a development run with local sign-in."""

import os

os.environ.setdefault("HUB_DEBUG", "1")
os.environ["HUB_SIGN_IN"] = "local"

from hub.settings import *  # noqa: F403

# Jobs run where they are queued, so a test sees a job's outcome at once.

TASKS = {"default": {"BACKEND": "django.tasks.backends.immediate.ImmediateBackend"}}
