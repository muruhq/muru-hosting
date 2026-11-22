"""The hub's settings as the environment gives them."""

import tomllib
from pathlib import Path

import muruhosting_stubs
import pytest
from django.conf import settings
from django.db import connection

import hub.settings

ROOT = Path(__file__).resolve().parent.parent


def test_sqlite_is_the_database_without_a_database_url() -> None:
    if connection.vendor != "sqlite":
        pytest.skip("DATABASE_URL names another database")

    assert settings.DATABASES["default"]["OPTIONS"]["transaction_mode"] == "EXCLUSIVE"


@pytest.mark.postgres
@pytest.mark.django_db
def test_postgres_is_the_database_when_database_url_names_one() -> None:
    assert connection.vendor == "postgresql"

    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
        assert cursor.fetchone() == (1,)


def test_the_jobs_backend_is_the_database() -> None:
    assert hub.settings.TASKS["default"]["BACKEND"] == "django_tasks_db.DatabaseBackend"


def test_the_stubs_are_those_of_the_pinned_muru() -> None:
    project = tomllib.loads((Path(hub.settings.BASE_DIR) / "pyproject.toml").read_text())
    pins = [
        requirement.removeprefix("muructl==")
        for requirement in project["dependency-groups"]["dev"]
        if isinstance(requirement, str) and requirement.startswith("muructl==")
    ]

    assert pins == [muruhosting_stubs.MURU_VERSION], "run `just stubs` after upgrading Muru"


def test_each_example_is_a_project_a_site_can_build() -> None:
    examples = sorted(path for path in (ROOT / "examples").iterdir() if path.is_dir())

    assert [path.name for path in examples] == ["fastapi-ticker", "flask-guestbook"]

    for example in examples:
        settings = tomllib.loads((example / "pyproject.toml").read_text())["tool"]["muru"]

        assert settings["entrypoint"]
        assert settings["commands"]
        assert (example / "uv.lock").is_file()
