"""The hub's settings, all taken from the environment.

Specification sections 2 (the hub), 5.8 (local accounts) and 15.2 (the hub
on a laptop). Every setting that differs between a laptop and a deployment
is an environment variable, so one settings module serves both.
"""

import os
from pathlib import Path
from typing import Any

import dj_database_url
from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent


def _flag(name: str) -> bool:
    """Read an environment variable as a switch, off unless it says otherwise."""

    return os.environ.get(name, "").strip().lower() in {"1", "true", "yes", "on"}


def _data_dir() -> Path:
    """Find the directory for the hub's own files, and make sure it exists.

    Muru gives every application `MURU_DATA_DIR`. A command run outside Muru,
    such as the test suite, falls back to an ignored directory of the checkout.
    """

    path = Path(os.environ.get("MURU_DATA_DIR") or BASE_DIR / ".muru-hosting" / "hub")
    path.mkdir(parents=True, exist_ok=True)

    return path


DEBUG = _flag("HUB_DEBUG")

# The secret key comes from outside the code. A development run has a fixed
# one, so that sessions survive a reload.

SECRET_KEY = os.environ.get("HUB_SECRET_KEY", "")

if not SECRET_KEY:
    if not DEBUG:
        raise ImproperlyConfigured("HUB_SECRET_KEY must be set unless HUB_DEBUG is on.")

    SECRET_KEY = "development-only-not-a-secret"

ALLOWED_HOSTS = [
    host.strip()
    for host in os.environ.get("HUB_ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")
    if host.strip()
]

# How people sign in: `github`, or `local` for accounts held by Django's own
# authentication, which also turns the Django admin site on (section 5.8).

SIGN_IN_GITHUB = "github"
SIGN_IN_LOCAL = "local"

HUB_SIGN_IN = os.environ.get("HUB_SIGN_IN", SIGN_IN_GITHUB)

if HUB_SIGN_IN not in {SIGN_IN_GITHUB, SIGN_IN_LOCAL}:
    raise ImproperlyConfigured(
        f"HUB_SIGN_IN must be {SIGN_IN_GITHUB!r} or {SIGN_IN_LOCAL!r}, not {HUB_SIGN_IN!r}."
    )

HUB_ADMIN_SITE = HUB_SIGN_IN == SIGN_IN_LOCAL

# A page may deploy a directory of the hub's own machine only on a
# developer's machine, which local sign-in stands for (section 15.3).

HUB_DEPLOY_FROM_DISK = HUB_SIGN_IN == SIGN_IN_LOCAL

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_tasks_db",
    "hub.accounts",
    "hub.hosting",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.auth.middleware.LoginRequiredMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "hub.urls"
WSGI_APPLICATION = "hub.wsgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "hub" / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "hub.accounts.context_processors.sign_in",
            ],
        },
    },
]

# SQLite in the data directory unless DATABASE_URL names Postgres (section
# 15.2). django-tasks-db needs exclusive transactions on SQLite, so that two
# workers never take the same job.

DATA_DIR = _data_dir()

DATABASES: dict[str, dict[str, Any]] = {
    "default": dict(
        dj_database_url.config(
            default=f"sqlite:///{DATA_DIR / 'hub.sqlite3'}",
            conn_max_age=60,
        )
    ),
}

if DATABASES["default"]["ENGINE"] == "django.db.backends.sqlite3":
    DATABASES["default"].setdefault("OPTIONS", {})["transaction_mode"] = "EXCLUSIVE"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Where the hub itself answers, for links to it from outside, and the hello
# site's project, which every new site is given (section 7.2).

HUB_URL = os.environ.get("HUB_URL", "http://127.0.0.1:9080")
HELLO_SITE_DIR = BASE_DIR / "hello"

# Jobs: Django's tasks framework on the database, run by `manage.py
# db_worker` (section 2.3).

TASKS = {
    "default": {
        "BACKEND": "django_tasks_db.DatabaseBackend",
    },
}

AUTH_USER_MODEL = "accounts.User"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LOGIN_URL = "sign-in"
LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "sign-in"

LANGUAGE_CODE = "en"
TIME_ZONE = "UTC"
USE_I18N = False
USE_TZ = True

# Static files are served by Muru's edge from the release's own static
# directory, which `collectstatic` fills before the workers start. A
# development run serves them from each application through the URLs.

STATIC_URL = "static/"
STATIC_ROOT = Path(os.environ.get("MURU_STATIC_DIR") or BASE_DIR / "staticfiles")
STATICFILES_DIRS = [BASE_DIR / "hub" / "static"]
