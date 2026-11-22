"""Run a site on this machine: a Muru daemon of its own and the site helper beside it.

Specification section 15.3. A local site has the parts of a site pod as
processes and directories of the developer's own:

- a daemon with its own state, run, log and configuration, so it never
  touches the developer's own daemon or another site's;

- the site directory, standing in for the pod's `site` claim;

- the helper under `muructl run`, told the admin socket, the site
  directory and its token.

Usage: local-site.py up OWNER/NAME
       local-site.py down OWNER/NAME
       local-site.py show OWNER/NAME

`up` starts both and prints the arguments for `manage.py register_site`,
which the `just site-up` recipe runs. `down` stops both and removes the
directories.
"""

from __future__ import annotations

import hashlib
import json
import os
import secrets
import shutil
import signal
import socket
import subprocess
import sys
import time
from dataclasses import asdict, dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITES = ROOT / ".muru-hosting" / "sites"
TEMPLATE = ROOT / "deploy" / "site" / "muru.toml"
HELPER = ROOT / "helper"


@dataclass(frozen=True)
class LocalSite:
    """Where a local site's parts are."""

    slug: str
    port: int
    helper_port: int
    helper_pid: int = 0

    @property
    def home(self) -> Path:
        """The site's directory in the checkout, holding everything but the run directory."""

        return SITES / self.slug.replace("/", "-")

    @property
    def run_dir(self) -> Path:
        """The daemon's run directory, short enough for a Unix socket's path.

        A socket path is limited to 104 bytes on macOS, which a path within
        a checkout easily passes, so it is under the system's temporary
        directory, named for the checkout and the site.
        """

        name = hashlib.sha256(str(self.home).encode()).hexdigest()[:10]

        return Path("/tmp") / f"muru-hosting-{os.getuid()}" / name

    @property
    def record(self) -> Path:
        """The file that keeps the site's ports and the helper's pid."""

        return self.home / "local-site.json"

    @property
    def token_file(self) -> Path:
        """The file holding the helper's token."""

        return self.home / "token"

    def daemon_flags(self) -> list[str]:
        """Return the flags that find this site's daemon, for every `muructl daemon` command."""

        return [
            "--state-dir",
            str(self.home / "state"),
            "--run-dir",
            str(self.run_dir),
            "--log-dir",
            str(self.home / "log"),
            "--config",
            str(self.home / "muru.toml"),
        ]

    def save(self) -> None:
        """Keep the site's ports and the helper's pid."""

        self.record.write_text(json.dumps(asdict(self), indent=2) + "\n")


def load(slug: str) -> LocalSite | None:
    """Read a local site's record, or None when there is no such site."""

    record = LocalSite(slug, 0, 0).record

    if not record.is_file():
        return None

    return LocalSite(**json.loads(record.read_text()))


def free_port() -> int:
    """Pick a port on loopback that nothing listens on now."""

    with socket.socket() as listener:
        listener.bind(("127.0.0.1", 0))

        return int(listener.getsockname()[1])


def listening(port: int) -> bool:
    """Say whether something accepts connections on a loopback port."""

    with socket.socket() as probe:
        probe.settimeout(0.5)

        return probe.connect_ex(("127.0.0.1", port)) == 0


def muructl(*arguments: str) -> subprocess.CompletedProcess[str]:
    """Run the pinned muructl, and fail with what it said."""

    result = subprocess.run(
        ["uv", "run", "--project", str(ROOT), "muructl", *arguments],
        capture_output=True,
        text=True,
        check=False,
    )

    if result.returncode != 0:
        raise SystemExit(
            f"muructl {' '.join(arguments[:2])} failed:\n{result.stdout}{result.stderr}"
        )

    return result


def up(slug: str) -> None:
    """Start a site's daemon and helper, or say that they are up already."""

    site = load(slug)

    if site is not None and listening(site.port) and listening(site.helper_port):
        print(f"{slug} is already up", file=sys.stderr)
        show(site)
        return

    if site is None:
        site = LocalSite(slug, port=free_port(), helper_port=free_port())

    # The directories and the files the two processes are told of.

    for directory in (site.home / "site" / "sources", site.home / "state", site.home / "log"):
        directory.mkdir(parents=True, exist_ok=True)

    site.run_dir.mkdir(parents=True, exist_ok=True)

    if not site.token_file.is_file():
        site.token_file.write_text(secrets.token_urlsafe(32) + "\n")
        site.token_file.chmod(0o600)

    (site.home / "muru.toml").write_text(
        TEMPLATE.read_text().format(listen=f"127.0.0.1:{site.port}")
    )

    # The daemon, which goes to the background by itself and answers before
    # the command returns.

    if not listening(site.port):
        muructl("daemon", "start", *site.daemon_flags())

    # The helper, a development run of its project, left running with its
    # output in the site's log directory.

    environment = os.environ | {
        "HELPER_ADMIN_SOCKET": str(site.run_dir / "admin.sock"),
        "HELPER_SITE_DIR": str(site.home / "site"),
        "HELPER_TOKEN_FILE": str(site.token_file),
    }

    with (site.home / "log" / "helper.log").open("ab") as log:
        helper = subprocess.Popen(
            [
                "uv",
                "run",
                "--project",
                str(ROOT),
                "muructl",
                "run",
                str(HELPER),
                "--port",
                str(site.helper_port),
            ],
            env=environment,
            stdout=log,
            stderr=subprocess.STDOUT,
            stdin=subprocess.DEVNULL,
            start_new_session=True,
        )

    site = LocalSite(site.slug, site.port, site.helper_port, helper.pid)
    site.save()

    deadline = time.monotonic() + 30

    while not listening(site.helper_port):
        if helper.poll() is not None or time.monotonic() > deadline:
            raise SystemExit(f"the helper did not start; see {site.home / 'log' / 'helper.log'}")

        time.sleep(0.2)

    show(site)


def show(site: LocalSite) -> None:
    """Print the arguments `manage.py register_site` takes for the site."""

    print(
        f"{site.slug} --helper 127.0.0.1:{site.helper_port} "
        f"--token-file {site.token_file} --site-dir {site.home / 'site'} "
        f"--url http://127.0.0.1:{site.port}/"
    )


def down(slug: str) -> None:
    """Stop a site's helper and daemon, and remove its directories."""

    site = load(slug)

    if site is None:
        raise SystemExit(f"there is no local site {slug}")

    # The helper runs in a session of its own, so its whole group is stopped.

    if site.helper_pid:
        try:
            os.killpg(site.helper_pid, signal.SIGTERM)
        except ProcessLookupError:
            pass

    if (site.run_dir / "admin.sock").exists():
        muructl("daemon", "stop", "--shutdown", *site.daemon_flags())

    shutil.rmtree(site.run_dir, ignore_errors=True)
    shutil.rmtree(site.home, ignore_errors=True)
    print(f"stopped {slug} and removed {site.home}", file=sys.stderr)


def main(arguments: list[str]) -> None:
    """Start, stop or show a local site."""

    if len(arguments) != 2 or arguments[0] not in {"up", "down", "show"} or "/" not in arguments[1]:
        raise SystemExit(__doc__)

    action, slug = arguments

    if action == "up":
        up(slug)
    elif action == "down":
        down(slug)
    else:
        site = load(slug)

        if site is None:
            raise SystemExit(f"there is no local site {slug}")

        show(site)


if __name__ == "__main__":
    main(sys.argv[1:])
