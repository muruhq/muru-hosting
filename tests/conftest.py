"""Fixtures and markers shared by the hub's tests."""

import os
import shutil
import socket
import subprocess
import tempfile
import time
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path

import pytest
from django.db import connection

from hub.accounts.models import User

ROOT = Path(__file__).resolve().parent.parent


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


@dataclass(frozen=True)
class RunningSite:
    """A real Muru daemon with the site helper beside it, for tests that need both."""

    helper_address: str
    token: str
    url: str
    site_dir: Path


def _free_port() -> int:
    with socket.socket() as listener:
        listener.bind(("127.0.0.1", 0))

        return int(listener.getsockname()[1])


def _wait_for(port: int, process: subprocess.Popen[bytes] | None, what: str) -> None:
    """Wait until something listens on a loopback port, or fail saying what did not start."""

    deadline = time.monotonic() + 60

    while time.monotonic() < deadline:
        with socket.socket() as probe:
            if probe.connect_ex(("127.0.0.1", port)) == 0:
                return

        if process is not None and process.poll() is not None:
            break

        time.sleep(0.2)

    raise RuntimeError(f"{what} did not start")


@pytest.fixture(scope="session")
def running_site(tmp_path_factory: pytest.TempPathFactory) -> Iterator[RunningSite]:
    """Run a daemon of its own and the helper under `muructl run`, as a local site has them.

    The parts are those of `scripts/local-site.py`: the daemon's state, log
    and configuration in a directory of their own, the run directory short
    enough for a Unix socket's path, and the helper told the admin socket,
    the site directory and its token.
    """

    home = tmp_path_factory.mktemp("site")
    run_dir = Path(tempfile.mkdtemp(prefix="mh-", dir="/tmp"))
    site_dir = home / "site"
    site_dir.mkdir()
    port, helper_port, token = _free_port(), _free_port(), "test-token"

    config = home / "muru.toml"
    config.write_text(
        (ROOT / "deploy" / "site" / "muru.toml").read_text().format(listen=f"127.0.0.1:{port}")
    )
    flags = [
        "--state-dir", str(home / "state"),
        "--run-dir", str(run_dir),
        "--log-dir", str(home / "log"),
        "--config", str(config),
    ]  # fmt: skip

    subprocess.run(["muructl", "daemon", "start", *flags], check=True, capture_output=True)

    helper = subprocess.Popen(
        ["muructl", "run", str(ROOT / "helper"), "--port", str(helper_port)],
        env=os.environ
        | {
            "HELPER_ADMIN_SOCKET": str(run_dir / "admin.sock"),
            "HELPER_SITE_DIR": str(site_dir),
            "HELPER_TOKEN": token,
        },
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    try:
        _wait_for(helper_port, helper, "the site helper")

        yield RunningSite(
            helper_address=f"127.0.0.1:{helper_port}",
            token=token,
            url=f"http://127.0.0.1:{port}/",
            site_dir=site_dir,
        )
    finally:
        helper.terminate()
        helper.wait(timeout=30)
        subprocess.run(
            ["muructl", "daemon", "stop", "--shutdown", *flags],
            check=False,
            capture_output=True,
        )
        shutil.rmtree(run_dir, ignore_errors=True)
