"""The site helper's parts that need no daemon: the token, the allowlist and the source store."""

import hashlib
import io
import tarfile
from pathlib import Path

import grpc
import pytest
from muruhosting_helper import allowlist, auth
from muruhosting_helper.sources import SourceError, SourceStore
from muruhosting_stubs.muru.admin.v1 import admin_pb2

SERVICE = admin_pb2.DESCRIPTOR.services_by_name["Admin"]


def archive(members: dict[str, bytes], *, extra: list[tarfile.TarInfo] | None = None) -> bytes:
    """Make a tar archive of files, with any further members as given."""

    buffer = io.BytesIO()

    with tarfile.open(fileobj=buffer, mode="w:gz") as tar:
        for name, data in members.items():
            info = tarfile.TarInfo(name)
            info.size = len(data)
            tar.addfile(info, io.BytesIO(data))

        for info in extra or []:
            tar.addfile(info)

    return buffer.getvalue()


def upload(store: SourceStore, name: str, data: bytes, sha256: str | None = None) -> None:
    store.upload(name, sha256 or hashlib.sha256(data).hexdigest(), "", iter([data]))


@pytest.fixture
def store(tmp_path: Path) -> SourceStore:
    """Make a source store in an empty directory."""

    return SourceStore(tmp_path / "sources", max_bytes=1024 * 1024)


def test_the_token_is_a_bearer_credential() -> None:
    assert auth.authorised([("authorization", "Bearer s3cret")], "s3cret")
    assert auth.authorised([("Authorization", b"bearer s3cret")], "s3cret")
    assert not auth.authorised([("authorization", "Bearer other")], "s3cret")
    assert not auth.authorised([("authorization", "s3cret")], "s3cret")
    assert not auth.authorised([], "s3cret")
    assert not auth.authorised(None, "s3cret")


def test_every_allowed_call_is_one_the_pinned_muru_has() -> None:
    assert allowlist.ALLOWED <= {method.name for method in SERVICE.methods}


@pytest.mark.parametrize(
    "method",
    ["Shutdown", "UpgradeDaemon", "ReloadConfig", "RemoveApp", "DashboardLogin", "ClearCache"],
)
def test_calls_that_reach_past_a_site_are_refused(method: str) -> None:
    assert allowlist.refusal(method, b"") == f"{method} is not a call the hub may make"


def test_a_call_muru_adds_later_is_refused_until_it_is_listed() -> None:
    assert allowlist.refusal("SomethingNew", b"") is not None


def test_a_declared_command_runs_and_one_off_code_does_not() -> None:
    declared = admin_pb2.RunCommandRequest(app="site", name="migrate").SerializeToString()
    one_off = admin_pb2.RunCommandRequest(app="site", argv=["id"]).SerializeToString()
    both = admin_pb2.RunCommandRequest(app="site", name="migrate", argv=["id"]).SerializeToString()

    assert allowlist.refusal("RunCommand", declared) is None
    assert allowlist.refusal("RunCommand", one_off) is not None
    assert allowlist.refusal("RunCommand", both) is not None


def test_debug_looks_and_restarts_but_does_not_inspect() -> None:
    def debug(op: str) -> bytes:
        return bytes(admin_pb2.DebugRequest(app="site", op=op).SerializeToString())

    assert allowlist.refusal("Debug", debug("stacks")) is None
    assert allowlist.refusal("Debug", debug("restart")) is None
    assert allowlist.refusal("Debug", debug("inspect")) is not None
    assert allowlist.refusal("Debug", debug("memory")) is not None


def test_an_archive_is_unpacked_into_a_directory_named_for_it(store: SourceStore) -> None:
    upload(store, "abc123", archive({"app.py": b"print()", "pkg/mod.py": b""}))

    assert (store.sources_dir / "abc123" / "app.py").read_bytes() == b"print()"
    assert (store.sources_dir / "abc123" / "pkg" / "mod.py").is_file()
    assert [record.name for record in store.records()] == ["abc123"]


def test_an_archive_with_another_digest_is_refused_and_leaves_nothing(store: SourceStore) -> None:
    with pytest.raises(SourceError) as refused:
        upload(store, "abc123", archive({"app.py": b""}), sha256="0" * 64)

    assert refused.value.code == grpc.StatusCode.DATA_LOSS
    assert not (store.sources_dir / "abc123").exists()
    assert store.records() == []


def test_the_same_archive_uploaded_again_is_the_source_already_there(store: SourceStore) -> None:
    data = archive({"app.py": b""})
    upload(store, "abc123", data)
    upload(store, "abc123", data)

    assert len(store.records()) == 1


def test_another_archive_under_a_name_in_use_is_refused(store: SourceStore) -> None:
    upload(store, "abc123", archive({"app.py": b"one"}))

    with pytest.raises(SourceError) as refused:
        upload(store, "abc123", archive({"app.py": b"two"}))

    assert refused.value.code == grpc.StatusCode.ALREADY_EXISTS
    assert (store.sources_dir / "abc123" / "app.py").read_bytes() == b"one"


def link(name: str, target: str, kind: bytes = tarfile.SYMTYPE) -> tarfile.TarInfo:
    info = tarfile.TarInfo(name)
    info.type = kind
    info.linkname = target

    return info


def device(name: str) -> tarfile.TarInfo:
    info = tarfile.TarInfo(name)
    info.type = tarfile.CHRTYPE

    return info


@pytest.mark.parametrize(
    "data",
    [
        archive({"../escaped.py": b""}),
        archive({"/tmp/absolute.py": b""}),
        archive({}, extra=[link("out", "../../etc/passwd")]),
        archive({}, extra=[link("out", "/etc/passwd")]),
        archive({}, extra=[link("hard", "../outside", tarfile.LNKTYPE)]),
        archive({}, extra=[device("null")]),
        b"not a tar archive",
    ],
    ids=["dot-dot", "absolute", "link-out", "link-absolute", "hard-link-out", "device", "not-tar"],
)
def test_an_archive_that_reaches_outside_its_directory_is_refused(
    store: SourceStore, data: bytes
) -> None:
    with pytest.raises(SourceError) as refused:
        upload(store, "abc123", data)

    assert refused.value.code == grpc.StatusCode.INVALID_ARGUMENT
    assert not (store.sources_dir / "abc123").exists()
    assert not (store.sources_dir.parent / "escaped.py").exists()


def test_a_link_within_the_directory_is_kept(store: SourceStore) -> None:
    upload(store, "abc123", archive({"app.py": b""}, extra=[link("alias.py", "app.py")]))

    assert (store.sources_dir / "abc123" / "alias.py").is_symlink()


def test_an_archive_past_the_limit_is_refused(tmp_path: Path) -> None:
    small = SourceStore(tmp_path / "sources", max_bytes=10)

    with pytest.raises(SourceError) as refused:
        upload(small, "abc123", archive({"app.py": b"x" * 100}))

    assert refused.value.code == grpc.StatusCode.RESOURCE_EXHAUSTED


@pytest.mark.parametrize("name", ["", ".", "..", ".hidden", "a/b", "../up", "-flag", "x" * 101])
def test_a_name_that_is_not_a_plain_one_is_refused(store: SourceStore, name: str) -> None:
    with pytest.raises(SourceError) as refused:
        upload(store, name, archive({"app.py": b""}))

    assert refused.value.code == grpc.StatusCode.INVALID_ARGUMENT


def test_a_source_is_removed_with_its_record(store: SourceStore) -> None:
    upload(store, "abc123", archive({"app.py": b""}))
    store.remove("abc123")

    assert not (store.sources_dir / "abc123").exists()
    assert store.records() == []

    with pytest.raises(SourceError) as missing:
        store.remove("abc123")

    assert missing.value.code == grpc.StatusCode.NOT_FOUND
