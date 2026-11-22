"""The helper and the hub's deploys against a real Muru daemon, as a local site runs them."""

import itertools
import urllib.request
from pathlib import Path

import grpc
import pytest
from muruhosting_stubs.muru.admin.v1 import admin_pb2, admin_pb2_grpc
from muruhosting_stubs.muruhosting.site.v1 import sources_pb2, sources_pb2_grpc

from hub.accounts.models import User
from hub.hosting import services
from hub.hosting.models import Deploy, Site
from tests.conftest import RunningSite


def fetch(url: str) -> str:
    with urllib.request.urlopen(url, timeout=10) as response:
        return str(response.read().decode())


@pytest.fixture
def admin_api(running_site: RunningSite) -> admin_pb2_grpc.AdminStub:
    """Make a client of the admin API through the helper, without the token."""

    return admin_pb2_grpc.AdminStub(grpc.insecure_channel(running_site.helper_address))


@pytest.fixture
def token(running_site: RunningSite) -> list[tuple[str, str]]:
    """Make the metadata that carries the helper's token."""

    return [("authorization", f"Bearer {running_site.token}")]


def test_a_call_without_the_token_is_refused(
    admin_api: admin_pb2_grpc.AdminStub, running_site: RunningSite
) -> None:
    sources = sources_pb2_grpc.SourcesStub(grpc.insecure_channel(running_site.helper_address))

    with pytest.raises(grpc.RpcError) as proxied:
        admin_api.GetStatus(admin_pb2.GetStatusRequest(), timeout=10)

    with pytest.raises(grpc.RpcError) as own:
        sources.ListSources(sources_pb2.ListSourcesRequest(), timeout=10)

    assert proxied.value.code() == grpc.StatusCode.UNAUTHENTICATED
    assert own.value.code() == grpc.StatusCode.UNAUTHENTICATED


def test_an_allowed_call_reaches_the_daemon_and_its_answer_comes_back_unchanged(
    admin_api: admin_pb2_grpc.AdminStub, token: list[tuple[str, str]]
) -> None:
    status = admin_api.GetStatus(admin_pb2.GetStatusRequest(), metadata=token, timeout=10)

    assert status.kind == "daemon"
    assert status.socket.endswith("admin.sock")


def test_the_daemons_own_refusal_comes_back_with_its_status(
    admin_api: admin_pb2_grpc.AdminStub, token: list[tuple[str, str]]
) -> None:
    with pytest.raises(grpc.RpcError) as missing:
        admin_api.GetApp(admin_pb2.GetAppRequest(name="nowhere"), metadata=token, timeout=10)

    assert missing.value.code() == grpc.StatusCode.NOT_FOUND
    assert "nowhere" in (missing.value.details() or "")


def test_a_call_off_the_allowlist_never_reaches_the_daemon(
    admin_api: admin_pb2_grpc.AdminStub, token: list[tuple[str, str]]
) -> None:
    with pytest.raises(grpc.RpcError) as refused:
        admin_api.Shutdown(admin_pb2.ShutdownRequest(), metadata=token, timeout=10)

    assert refused.value.code() == grpc.StatusCode.PERMISSION_DENIED

    # The daemon is still there to answer.

    assert admin_api.GetStatus(admin_pb2.GetStatusRequest(), metadata=token, timeout=10).pid


def test_one_off_code_is_refused_on_a_streaming_call(
    admin_api: admin_pb2_grpc.AdminStub, token: list[tuple[str, str]]
) -> None:
    run = admin_pb2.RunCommandRequest(app="site", argv=["id"])

    with pytest.raises(grpc.RpcError) as refused:
        list(admin_api.RunCommand(run, metadata=token, timeout=10))

    assert refused.value.code() == grpc.StatusCode.PERMISSION_DENIED


def test_a_stream_is_forwarded(
    admin_api: admin_pb2_grpc.AdminStub, token: list[tuple[str, str]]
) -> None:
    events = admin_api.WatchEvents(admin_pb2.WatchEventsRequest(), metadata=token, timeout=10)
    first = next(iter(itertools.islice(events, 1)))
    events.cancel()

    assert first.type == "daemon.started"


@pytest.mark.django_db(transaction=True)
def test_a_registered_site_gets_the_hello_site_and_then_a_deploy_of_a_directory(
    running_site: RunningSite, member: User, tmp_path: Path
) -> None:
    site = services.register_local_site(
        member,
        "blog",
        running_site.helper_address,
        running_site.token,
        running_site.url,
        str(running_site.site_dir),
    )

    # The job ran where it was queued: the hello site is release r1.

    site.refresh_from_db()
    hello = site.deploys.get()

    assert (site.state, site.state_message) == (Site.State.READY, "")
    assert (hello.state, hello.release, hello.message) == (Deploy.State.SERVING, "r1", "")

    page = fetch(running_site.url)

    assert "alice/blog is up" in page
    assert "<code>r1</code>" in page
    assert "/sites/alice/blog/" in page
    assert "--accent" in fetch(running_site.url + "static/hello.css")

    # The site's data directory is on the site's own directory.

    assert (running_site.site_dir / "data").is_dir()

    # A project of the owner's own becomes r2, with nothing of the hello site.

    project = tmp_path / "project"
    project.mkdir()
    (project / "pyproject.toml").write_text(
        '[project]\nname = "mine"\nversion = "0"\n\n[tool.muru]\nentrypoint = "mine:application"\n'
    )
    (project / "mine.py").write_text(
        "import os\n\n"
        "def application(environ, start_response):\n"
        "    start_response('200 OK', [('Content-Type', 'text/plain')])\n"
        "    return [f\"mine {os.environ.get('HELLO_SITE')}\".encode()]\n"
    )

    deploy = services.deploy_directory(site, project)
    deploy.refresh_from_db()

    assert (deploy.state, deploy.release, deploy.message) == (Deploy.State.SERVING, "r2", "")
    assert fetch(running_site.url) == "mine None"

    live = services.live_site(site)

    assert [(release.id, release.serving) for release in live.releases] == [
        ("r2", True),
        ("r1", False),
    ]
    assert live.error == ""
