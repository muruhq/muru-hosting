"""Source archives: a directory made into the tar file a site's helper unpacks."""

from __future__ import annotations

import gzip
import hashlib
import io
import subprocess
import tarfile
from dataclasses import dataclass
from pathlib import Path

# What is never part of a source: version control, environments and caches.

EXCLUDED = frozenset(
    {".git", ".venv", "__pycache__", ".mypy_cache", ".pytest_cache", ".ruff_cache"}
)


@dataclass(frozen=True)
class Archive:
    """A source archive and what names it."""

    data: bytes
    sha256: str
    commit: str = ""


def _tidy(member: tarfile.TarInfo) -> tarfile.TarInfo | None:
    """Leave out what is never part of a source, and whatever would make two archives differ."""

    if any(part in EXCLUDED for part in Path(member.name).parts):
        return None

    member.uid = member.gid = 0
    member.uname = member.gname = ""
    member.mtime = 0

    return member


def archive_directory(directory: Path) -> Archive:
    """Make a directory into a gzipped tar archive, the same bytes for the same files."""

    buffer = io.BytesIO()

    # The gzip header and every member carry no time or owner, so that a
    # directory's archive, and the digest that names it, depend on its files
    # alone.

    with (
        gzip.GzipFile(fileobj=buffer, mode="wb", mtime=0) as compressed,
        tarfile.open(fileobj=compressed, mode="w") as tar,
    ):
        for path in sorted(directory.rglob("*")):
            tar.add(path, arcname=str(path.relative_to(directory)), recursive=False, filter=_tidy)

    data = buffer.getvalue()

    return Archive(data=data, sha256=hashlib.sha256(data).hexdigest(), commit=commit_of(directory))


def commit_of(directory: Path) -> str:
    """Return the commit a directory is a clean checkout of, or nothing.

    A directory with uncommitted changes, or one that is not the top of a
    git checkout, has no commit to record.
    """

    def git(*arguments: str) -> str | None:
        result = subprocess.run(
            ["git", "-C", str(directory), *arguments],
            capture_output=True,
            text=True,
            check=False,
        )

        return result.stdout.strip() if result.returncode == 0 else None

    top = git("rev-parse", "--show-toplevel")

    if top is None or Path(top).resolve() != directory.resolve():
        return ""

    if git("status", "--porcelain") != "":
        return ""

    return git("rev-parse", "HEAD") or ""
