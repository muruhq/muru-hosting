"""The Sources service: a release's code, uploaded as a tar archive.

Specification section 4.3. Muru's `Deploy` takes a directory the daemon
reads, so the hub uploads an archive here and deploys the directory it is
unpacked into. The service is removed when Muru can take a release's code
through its own API (muruhq/muru#865).
"""

from __future__ import annotations

import hashlib
import hmac
import json
import re
import shutil
import tarfile
import tempfile
import time
from collections.abc import Iterator
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import grpc
from muruhosting_stubs.muruhosting.site.v1 import sources_pb2, sources_pb2_grpc

from muruhosting_helper import auth
from muruhosting_helper.settings import Settings

NAME = re.compile(r"[A-Za-z0-9_][A-Za-z0-9._-]{0,99}")

# Where the record of each source is kept, apart from the sources themselves
# so that a release's directory holds the archive's files and nothing else.

RECORDS = ".records"


class SourceError(Exception):
    """An upload or removal that is refused, with the status to answer."""

    def __init__(self, code: grpc.StatusCode, details: str) -> None:
        super().__init__(details)
        self.code = code
        self.details = details


@dataclass(frozen=True)
class Record:
    """What the helper keeps about a source directory."""

    name: str
    commit: str
    sha256: str
    created_unix: int


class SourceStore:
    """The source directories beneath a site's `sources/`."""

    def __init__(self, sources_dir: Path, max_bytes: int) -> None:
        self.sources_dir = sources_dir
        self.max_bytes = max_bytes

    def path(self, name: str) -> Path:
        """Return a source's directory, refusing a name that is not a plain one."""

        if NAME.fullmatch(name) is None or name == RECORDS:
            raise SourceError(
                grpc.StatusCode.INVALID_ARGUMENT,
                "a source's name is letters, digits, dots, hyphens and underscores, "
                "at most 100, and does not start with a dot or a hyphen",
            )

        return self.sources_dir / name

    def _record_path(self, name: str) -> Path:
        return self.sources_dir / RECORDS / f"{name}.json"

    def record(self, name: str) -> Record | None:
        """Return what is kept about a source, or None when there is no such source."""

        path = self._record_path(name)

        if not path.is_file() or not (self.sources_dir / name).is_dir():
            return None

        return Record(**json.loads(path.read_text()))

    def records(self) -> list[Record]:
        """List the sources, oldest first."""

        directory = self.sources_dir / RECORDS

        if not directory.is_dir():
            return []

        names = sorted(path.stem for path in directory.glob("*.json"))
        found = [record for name in names if (record := self.record(name)) is not None]

        return sorted(found, key=lambda record: (record.created_unix, record.name))

    def upload(self, name: str, sha256: str, commit: str, chunks: Iterator[bytes]) -> Record:
        """Unpack an archive into the directory named, and return its record.

        The archive is checked against `sha256` before anything is unpacked.
        Uploading a source that is already there with the same digest answers
        with the one there, so a job that is run again does no harm.
        """

        target = self.path(name)
        existing = self.record(name)

        if existing is not None and existing.sha256 != sha256.lower():
            raise SourceError(
                grpc.StatusCode.ALREADY_EXISTS,
                f"the source {name} exists and was unpacked from another archive",
            )

        (self.sources_dir / RECORDS).mkdir(parents=True, exist_ok=True)

        # The archive goes to a file first, so that its digest is known
        # before any of it is unpacked.

        with tempfile.TemporaryDirectory(dir=self.sources_dir, prefix=".incoming-") as scratch:
            archive = Path(scratch) / "source.tar"
            self._receive(archive, sha256, chunks)

            if existing is not None:
                return existing

            unpacked = Path(scratch) / "unpacked"
            self._unpack(archive, unpacked)

            if target.exists():
                shutil.rmtree(target)

            unpacked.rename(target)

        record = Record(
            name=name, commit=commit, sha256=sha256.lower(), created_unix=int(time.time())
        )
        self._record_path(name).write_text(json.dumps(asdict(record)))

        return record

    def _receive(self, archive: Path, sha256: str, chunks: Iterator[bytes]) -> None:
        """Write the chunks to a file, refusing one too large or with another digest."""

        digest = hashlib.sha256()
        size = 0

        with archive.open("wb") as file:
            for chunk in chunks:
                size += len(chunk)

                if size > self.max_bytes:
                    raise SourceError(
                        grpc.StatusCode.RESOURCE_EXHAUSTED,
                        f"the archive is larger than {self.max_bytes} bytes",
                    )

                digest.update(chunk)
                file.write(chunk)

        if not hmac.compare_digest(digest.hexdigest(), sha256.lower()):
            raise SourceError(
                grpc.StatusCode.DATA_LOSS,
                f"the archive's SHA-256 is {digest.hexdigest()}, not the {sha256} expected",
            )

    def _unpack(self, archive: Path, directory: Path) -> None:
        """Unpack an archive, refusing whatever would reach outside the directory.

        tarfile's `data` filter refuses `..`, links that lead out of the
        directory and device files, and drops set-user-id bits. It makes an
        absolute path relative where the helper is to refuse it, so those
        are looked for first.
        """

        directory.mkdir()

        try:
            with tarfile.open(archive, mode="r:*") as tar:
                for member in tar:
                    if member.name.startswith(("/", "\\")):
                        raise tarfile.TarError(f"{member.name!r} is an absolute path")

            with tarfile.open(archive, mode="r:*") as tar:
                tar.extractall(directory, filter="data")
        except (tarfile.TarError, OSError) as error:
            raise SourceError(
                grpc.StatusCode.INVALID_ARGUMENT, f"the archive cannot be unpacked: {error}"
            ) from error

    def remove(self, name: str) -> None:
        """Remove a source's directory and its record."""

        target = self.path(name)

        if self.record(name) is None:
            raise SourceError(grpc.StatusCode.NOT_FOUND, f"there is no source {name}")

        self._record_path(name).unlink()
        shutil.rmtree(target)


class SourcesServicer(sources_pb2_grpc.SourcesServicer):
    """muruhosting.site.v1.Sources, over a site's source store."""

    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._store = SourceStore(settings.sources_dir, settings.max_source_bytes)

    def _admit(self, context: Any) -> None:
        """End the call unless it carries the token."""

        if not auth.authorised(context.invocation_metadata(), self._settings.token):
            context.abort(grpc.StatusCode.UNAUTHENTICATED, auth.REFUSAL)

    def _source(self, record: Record) -> sources_pb2.Source:
        return sources_pb2.Source(
            name=record.name,
            path=str(self._store.path(record.name)),
            commit=record.commit,
            sha256=record.sha256,
            created_unix=record.created_unix,
        )

    def UploadSource(
        self, request_iterator: Iterator[sources_pb2.UploadSourceRequest], context: Any
    ) -> sources_pb2.Source:
        """Unpack the archive the stream carries, after its header."""

        self._admit(context)
        first = next(request_iterator, None)

        if first is None or first.WhichOneof("part") != "header":
            context.abort(
                grpc.StatusCode.INVALID_ARGUMENT, "the first message of an upload is its header"
            )
            raise AssertionError("abort ends the call")

        header = first.header

        def chunks() -> Iterator[bytes]:
            for message in request_iterator:
                if message.WhichOneof("part") != "chunk":
                    raise SourceError(
                        grpc.StatusCode.INVALID_ARGUMENT,
                        "an upload has one header, then chunks of the archive",
                    )

                yield message.chunk

        try:
            record = self._store.upload(header.name, header.sha256, header.commit, chunks())
        except SourceError as error:
            context.abort(error.code, error.details)

        return self._source(record)

    def ListSources(
        self, request: sources_pb2.ListSourcesRequest, context: Any
    ) -> sources_pb2.ListSourcesResponse:
        """List the source directories, oldest first."""

        self._admit(context)

        return sources_pb2.ListSourcesResponse(
            sources=[self._source(record) for record in self._store.records()]
        )

    def RemoveSource(
        self, request: sources_pb2.RemoveSourceRequest, context: Any
    ) -> sources_pb2.RemoveSourceResponse:
        """Remove one source directory."""

        self._admit(context)

        try:
            self._store.remove(request.name)
        except SourceError as error:
            context.abort(error.code, error.details)

        return sources_pb2.RemoveSourceResponse()
