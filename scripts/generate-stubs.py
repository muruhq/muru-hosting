"""Generate the gRPC stubs from the pinned Muru release's admin.proto and the helper's own.

The admin API's `.proto` file is fetched from Muru's repository at the tag
of the `muructl` release pinned in pyproject.toml, since the published
packages do not carry it (muruhq/muru#858; #28 here). It is kept in the stubs
package beside the generated code, so that an upgrade of Muru shows what
changed in the API.

Usage: generate-stubs.py [--no-fetch]

With --no-fetch, the stubs are generated from the admin.proto already in
the repository, which must be the pinned release's.
"""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
import tempfile
import tomllib
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STUBS = ROOT / "packages" / "stubs"
PROTO = STUBS / "proto"
PACKAGE = STUBS / "src" / "muruhosting_stubs"
ADMIN_PROTO = Path("muru/admin/v1/admin.proto")
VERSION_FILE = PACKAGE / "MURU_VERSION"

RAW = "https://raw.githubusercontent.com/muruhq/muru/{tag}/proto/{path}"


def pinned_version() -> str:
    """Read the `muructl` release pinned in pyproject.toml, as PyPI spells it."""

    project = tomllib.loads((ROOT / "pyproject.toml").read_text())

    for group in project["dependency-groups"].values():
        for requirement in group:
            match = (
                re.fullmatch(r"muructl==(\S+)", requirement)
                if isinstance(requirement, str)
                else None
            )

            if match:
                return match.group(1)

    raise SystemExit("pyproject.toml pins no muructl release")


def tag_of(version: str) -> str:
    """Turn a PyPI version such as 0.1.0a34 into the release's tag, v0.1.0-alpha.34."""

    match = re.fullmatch(r"(\d+\.\d+\.\d+)(?:(a|b|rc)(\d+))?", version)

    if match is None:
        raise SystemExit(f"cannot work out the tag of muructl {version}")

    release, phase, number = match.groups()

    if phase is None:
        return f"v{release}"

    return f"v{release}-{ {'a': 'alpha', 'b': 'beta', 'rc': 'rc'}[phase] }.{number}"


def fetch(version: str) -> None:
    """Fetch the admin API's `.proto` file of a Muru release into the stubs package."""

    url = RAW.format(tag=tag_of(version), path=ADMIN_PROTO)
    target = PROTO / ADMIN_PROTO
    target.parent.mkdir(parents=True, exist_ok=True)

    with urllib.request.urlopen(url) as response:
        target.write_bytes(response.read())

    print(f"fetched {ADMIN_PROTO} from {url}")


def generate() -> None:
    """Run protoc over every `.proto` file, with the modules beneath muruhosting_stubs."""

    # protoc names a module for its file's path, so the files are copied
    # beneath a directory named for the package: muru/admin/v1/admin.proto
    # becomes muruhosting_stubs.muru.admin.v1.admin_pb2, which cannot meet
    # Muru's own `muru` package.

    with tempfile.TemporaryDirectory() as scratch:
        tree = Path(scratch) / "muruhosting_stubs"
        shutil.copytree(PROTO, tree)
        files = sorted(str(path.relative_to(scratch)) for path in tree.rglob("*.proto"))

        for generated in ("muru", "muruhosting"):
            shutil.rmtree(PACKAGE / generated, ignore_errors=True)

        subprocess.run(
            [
                sys.executable,
                "-m",
                "grpc_tools.protoc",
                f"--proto_path={scratch}",
                f"--python_out={PACKAGE.parent}",
                f"--pyi_out={PACKAGE.parent}",
                f"--grpc_python_out={PACKAGE.parent}",
                *files,
            ],
            check=True,
        )

    print(f"generated stubs for {', '.join(files)}")


def main(arguments: list[str]) -> None:
    """Fetch the pinned release's admin.proto unless told not to, then generate."""

    version = pinned_version()

    if "--no-fetch" not in arguments:
        fetch(version)

    generate()
    VERSION_FILE.write_text(version + "\n")
    print(f"the admin API's stubs are those of muructl {version}")


if __name__ == "__main__":
    main(sys.argv[1:])
