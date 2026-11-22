"""The helper's settings, from the environment.

A site pod and a site on a laptop give the helper the same things: where
the daemon's admin socket is, where the site's directory is, and the token
the hub presents (specification sections 3.1 and 15.3). Nothing tells a
process beside a daemon where its admin socket is (muruhq/muru#867), so it
is a setting.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

DEFAULT_MAX_SOURCE_BYTES = 256 * 1024 * 1024


class SettingsError(RuntimeError):
    """The environment does not give the helper what it needs to start."""


@dataclass(frozen=True)
class Settings:
    """What the helper is told about the site it serves."""

    admin_socket: Path
    """The daemon's admin socket."""

    site_dir: Path
    """The site's directory, at the path the daemon reads it by."""

    token: str
    """The bearer token every call must carry."""

    max_source_bytes: int = DEFAULT_MAX_SOURCE_BYTES
    """The largest source archive an upload may send."""

    @property
    def sources_dir(self) -> Path:
        """Where each uploaded source has its directory."""

        return self.site_dir / "sources"


def _required(name: str) -> str:
    """Read a variable that must be set."""

    value = os.environ.get(name, "").strip()

    if not value:
        raise SettingsError(f"{name} must be set")

    return value


def _token() -> str:
    """Read the token from HELPER_TOKEN, or from the file HELPER_TOKEN_FILE names."""

    token = os.environ.get("HELPER_TOKEN", "").strip()

    if token:
        return token

    path = os.environ.get("HELPER_TOKEN_FILE", "").strip()

    if not path:
        raise SettingsError("HELPER_TOKEN or HELPER_TOKEN_FILE must be set")

    token = Path(path).read_text().strip()

    if not token:
        raise SettingsError(f"{path}, which HELPER_TOKEN_FILE names, is empty")

    return token


def load() -> Settings:
    """Read the helper's settings from the environment, or say what is missing."""

    return Settings(
        admin_socket=Path(_required("HELPER_ADMIN_SOCKET")),
        site_dir=Path(_required("HELPER_SITE_DIR")),
        token=_token(),
        max_source_bytes=int(os.environ.get("HELPER_MAX_SOURCE_BYTES") or DEFAULT_MAX_SOURCE_BYTES),
    )
