"""The deploy job and the site page, with a stand-in for the site's helper."""

import subprocess
from collections.abc import Iterator
from pathlib import Path

import grpc
import pytest
import wrapture
from django.core.management import CommandError, call_command
from django.test import Client
from muruhosting_stubs.muru.admin.v1 import admin_pb2
from wrapture import Tape

from hub.accounts.models import User
from hub.hosting import archives, services, tasks
from hub.hosting.helper import HelperClient, HelperError
from hub.hosting.models import Deploy, Site


class Unreachable(grpc.RpcError):
    """What grpc raises when nothing answers at the helper's address."""

    def code(self) -> grpc.StatusCode:
        return grpc.StatusCode.UNAVAILABLE

    def details(self) -> str:
        return "failed to connect to all addresses"


@pytest.fixture
def helper() -> Iterator[HelperClient]:
    """Stand in for every helper client the hub makes, with a daemon that deploys at once."""

    double = wrapture.mock(HelperClient)
    double.status.returns(admin_pb2.Status(version="0.1.0-test"))
    double.apply_config.returns(admin_pb2.ConfigReport(applied=True))
    double.upload_source.returns("/srv/site/sources/hello")
    double.plan_deploy.returns(admin_pb2.DeployPlan(release="r1"))
    double.release.returns(None)
    double.wait_release.returns(admin_pb2.Release(id="r1", state="ready", serving=True))
    double.releases.returns([])

    def make(address: str, token: str) -> HelperClient:
        return double  # type: ignore[no-any-return]

    with (
        wrapture.binding(tasks, attr="HelperClient").overrides(make),
        wrapture.binding(services, attr="HelperClient").overrides(make),
    ):
        yield double


@pytest.fixture
def site(member: User, helper: HelperClient, django_capture_on_commit_callbacks: object) -> Site:
    """Register a local site, whose hello deploy has run against the stand-in."""

    with django_capture_on_commit_callbacks(execute=True):  # type: ignore[operator]
        return services.register_local_site(
            member, "blog", "127.0.0.1:1", "token", "http://127.0.0.1:2/", "/srv/site"
        )


def test_registering_a_site_deploys_the_hello_site_in_order(site: Site, tape: Tape) -> None:
    site.refresh_from_db()
    deploy = site.deploys.get()

    assert site.state == Site.State.READY
    assert (deploy.state, deploy.release) == (Deploy.State.SERVING, "r1")
    assert deploy.source_name.startswith("hello-")
    assert deploy.env == {
        "HELLO_SITE": "alice/blog",
        "HELLO_HUB_URL": "http://127.0.0.1:9080/sites/alice/blog/",
    }


def test_the_job_takes_a_deploy_through_its_steps(
    member: User, helper: HelperClient, tape: Tape, django_capture_on_commit_callbacks: object
) -> None:
    with django_capture_on_commit_callbacks(execute=True):  # type: ignore[operator]
        services.register_local_site(
            member, "blog", "127.0.0.1:1", "token", "http://127.0.0.1:2/", "/srv/site"
        )

    tape.assert_order(
        tape.blocks("job:deploy"),
        tape.where(label="HelperClient.status"),
        tape.where(label="HelperClient.apply_config"),
        tape.where(label="HelperClient.upload_source"),
        tape.where(label="HelperClient.plan_deploy"),
        tape.where(label="HelperClient.deploy"),
        tape.where(label="HelperClient.wait_release"),
    )

    tape.where(label="HelperClient.apply_config").with_args(
        document='[app.site]\ndata_dir = "/srv/site/data"\n'
    ).assert_once()


def test_a_release_that_fails_to_start_fails_the_site(
    member: User, helper: HelperClient, django_capture_on_commit_callbacks: object
) -> None:
    helper.wait_release.returns(  # type: ignore[attr-defined]
        admin_pb2.Release(id="r1", state="failed", message="ModuleNotFoundError: hello")
    )

    with django_capture_on_commit_callbacks(execute=True):  # type: ignore[operator]
        site = services.register_local_site(
            member, "blog", "127.0.0.1:1", "token", "http://127.0.0.1:2/", "/srv/site"
        )

    site.refresh_from_db()

    assert site.state == Site.State.FAILED
    assert site.state_message == "ModuleNotFoundError: hello"
    assert site.deploys.get().state == Deploy.State.FAILED


def test_what_muru_would_refuse_is_never_deployed(
    site: Site,
    helper: HelperClient,
    tmp_path: Path,
    tape: Tape,
    django_capture_on_commit_callbacks: object,
) -> None:
    helper.plan_deploy.returns(  # type: ignore[attr-defined]
        admin_pb2.DeployPlan(release="r2", refusals=["no entrypoint is named"])
    )
    before = tape.where(label="HelperClient.deploy").count

    with django_capture_on_commit_callbacks(execute=True):  # type: ignore[operator]
        deploy = services.deploy_directory(site, tmp_path)

    deploy.refresh_from_db()
    site.refresh_from_db()

    assert (deploy.state, deploy.message) == (Deploy.State.FAILED, "no entrypoint is named")
    assert tape.where(label="HelperClient.deploy").count == before

    # A failed deploy leaves a site that was ready as it was.

    assert site.state == Site.State.READY


def test_a_helper_that_does_not_answer_fails_the_deploy_with_why(
    site: Site, helper: HelperClient, tmp_path: Path, django_capture_on_commit_callbacks: object
) -> None:
    helper.status.raises(HelperError("asking the site's daemon for its status", Unreachable()))  # type: ignore[attr-defined]

    with django_capture_on_commit_callbacks(execute=True):  # type: ignore[operator]
        deploy = services.deploy_directory(site, tmp_path)

    deploy.refresh_from_db()

    assert deploy.state == Deploy.State.FAILED
    assert "failed to connect" in deploy.message


def test_a_job_run_again_does_not_make_a_second_release(
    site: Site, helper: HelperClient, tape: Tape
) -> None:
    # The first run got as far as making the release, and stopped there.

    deploy = site.deploys.get()
    Deploy.objects.filter(pk=deploy.pk).update(state=Deploy.State.DEPLOYING)
    helper.release.returns(admin_pb2.Release(id="r1", state="ready"))  # type: ignore[attr-defined]

    # The tape starts here, so it holds the second run alone.

    tasks.run_deploy.call(deploy.pk)
    deploy.refresh_from_db()

    assert deploy.state == Deploy.State.SERVING
    tape.where(label="HelperClient.upload_source").assert_never()
    tape.where(label="HelperClient.deploy").assert_never()
    tape.where(label="HelperClient.wait_release").assert_once()


def test_the_site_page_shows_releases_with_what_the_hub_knows_of_them(
    client: Client, site: Site, helper: HelperClient, member: User
) -> None:
    helper.releases.returns(  # type: ignore[attr-defined]
        [
            admin_pb2.Release(id="r1", state="ready", serving=True, created_unix_ms=1795326180639),
            admin_pb2.Release(id="r0", state="stopped", created_unix_ms=1795326180000),
        ]
    )
    client.force_login(member)

    page = client.get("/sites/alice/blog/").text

    assert 'r1 <span class="tag">serving</span>' in page
    assert "The hello site" in page
    assert "Not deployed by the hub" in page
    assert "0.1.0-test" in page


def test_the_site_page_says_when_the_daemon_cannot_be_asked(
    client: Client, site: Site, helper: HelperClient, member: User
) -> None:
    helper.status.raises(HelperError("asking the site's daemon for its status", Unreachable()))  # type: ignore[attr-defined]
    client.force_login(member)

    response = client.get("/sites/alice/blog/")

    assert response.status_code == 200
    assert "could not be asked for its releases" in response.text


def test_a_site_someone_may_not_see_is_not_found(client: Client, site: Site, db: None) -> None:
    client.force_login(User.objects.create_user("bob", password="correct horse"))

    assert client.get("/sites/alice/blog/").status_code == 404


def test_an_admin_sees_any_site(client: Client, site: Site, admin: User) -> None:
    client.force_login(admin)

    assert client.get("/sites/alice/blog/").status_code == 200


def test_a_second_site_of_the_same_name_is_refused(site: Site, member: User) -> None:
    with pytest.raises(services.ActionRefused):
        services.register_local_site(member, "blog", "127.0.0.1:1", "t", "http://x/", "/srv/site")


def test_a_site_name_must_be_a_dns_label(member: User, helper: HelperClient) -> None:
    with pytest.raises(Exception, match="lower case"):
        services.register_local_site(member, "My_Blog", "127.0.0.1:1", "t", "http://x/", "/srv")


def test_register_site_needs_the_owners_account(db: None, tmp_path: Path) -> None:
    token = tmp_path / "token"
    token.write_text("t\n")

    with pytest.raises(CommandError, match="no account nobody"):
        call_command(
            "register_site", "nobody/blog", "--helper", "127.0.0.1:1",
            "--token-file", str(token), "--site-dir", "/srv/site", "--url", "http://x/",
        )  # fmt: skip


def test_forgetting_a_site_removes_it_and_its_deploys(site: Site) -> None:
    call_command("forget_site", "alice/blog")

    assert not Site.objects.exists()
    assert not Deploy.objects.exists()


def test_deploy_site_says_when_there_is_no_such_site(db: None, tmp_path: Path) -> None:
    with pytest.raises(CommandError, match="no site alice/nowhere"):
        call_command("deploy_site", "alice/nowhere", str(tmp_path))


def test_a_directorys_archive_is_the_same_bytes_each_time(tmp_path: Path) -> None:
    (tmp_path / "app.py").write_text("print()\n")
    (tmp_path / "__pycache__").mkdir()
    (tmp_path / "__pycache__" / "app.pyc").write_bytes(b"\0")

    first = archives.archive_directory(tmp_path)
    (tmp_path / "app.py").touch()
    second = archives.archive_directory(tmp_path)

    assert first.sha256 == second.sha256
    assert first.commit == ""


def git(directory: Path, *arguments: str) -> None:
    subprocess.run(
        ["git", "-C", str(directory), "-c", "user.name=t", "-c", "user.email=t@example.invalid",
         "-c", "commit.gpgsign=false", *arguments],
        check=True,
        capture_output=True,
    )  # fmt: skip


def test_the_commit_is_recorded_only_for_a_clean_checkout(tmp_path: Path) -> None:
    (tmp_path / "app.py").write_text("print()\n")
    git(tmp_path, "init", "-q")
    git(tmp_path, "add", ".")
    git(tmp_path, "commit", "-q", "-m", "first")

    clean = archives.archive_directory(tmp_path)
    (tmp_path / "app.py").write_text("print(1)\n")
    dirty = archives.archive_directory(tmp_path)

    assert len(clean.commit) == 40
    assert dirty.commit == ""
