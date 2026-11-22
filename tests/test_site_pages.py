"""What a person can do to a site from its page, with a stand-in for the site's helper."""

from pathlib import Path

import pytest
import wrapture
from django.test import Client
from muruhosting_stubs.muru.admin.v1 import admin_pb2
from wrapture import Tape

from hub.accounts.models import User
from hub.hosting import services
from hub.hosting.helper import HelperClient, HelperError
from hub.hosting.models import AuditEntry, Deploy, Site
from tests.conftest import Unreachable


@pytest.fixture
def served(site: Site, helper: HelperClient) -> Site:
    """Give the site a release that serves and an earlier one to go back to."""

    helper.app.returns(  # type: ignore[attr-defined]
        admin_pb2.App(name="site", current_release="r2", previous_release="r1")
    )
    helper.releases.returns(  # type: ignore[attr-defined]
        [
            admin_pb2.Release(id="r2", state="ready", serving=True, created_unix_ms=2000),
            admin_pb2.Release(id="r1", state="retained", created_unix_ms=1000),
        ]
    )

    return site


def test_the_page_offers_the_actions_to_someone_who_may_take_them(
    client: Client, served: Site, member: User
) -> None:
    client.force_login(member)

    page = client.get("/sites/alice/blog/").text

    assert "Roll back to r1" in page
    assert "Restart workers" in page
    assert "Turn maintenance on" in page
    assert 'action="/sites/alice/blog/releases/r1/promote/"' in page
    assert 'action="/sites/alice/blog/releases/r2/promote/"' not in page
    assert "A project's directory on this machine" in page


def test_rolling_back_asks_the_daemon_and_records_who_asked(
    client: Client, served: Site, helper: HelperClient, member: User, tape: Tape
) -> None:
    helper.rollback.returns(admin_pb2.Release(id="r1"))  # type: ignore[attr-defined]
    client.force_login(member)

    response = client.post("/sites/alice/blog/roll-back/", follow=True)

    assert "Traffic is going back to release r1." in response.text
    tape.where(label="HelperClient.rollback").assert_once()
    tape.where(label="sites.roll_back").assert_once()

    entry = AuditEntry.objects.get(action="roll-back")

    assert (entry.actor, entry.via, entry.succeeded) == (member, AuditEntry.Via.PAGE, True)
    assert "alice" in response.text


def test_serving_a_release_promotes_that_release(
    client: Client, served: Site, helper: HelperClient, member: User, tape: Tape
) -> None:
    helper.promote.returns(admin_pb2.Release(id="r1"))  # type: ignore[attr-defined]
    client.force_login(member)

    response = client.post("/sites/alice/blog/releases/r1/promote/", follow=True)

    assert "Traffic is going to release r1." in response.text
    tape.where(label="HelperClient.promote").with_args(release="r1").assert_once()
    assert AuditEntry.objects.get(action="promote").detail == "r1"


def test_restarting_replaces_each_worker_in_turn(
    client: Client, served: Site, helper: HelperClient, member: User, tape: Tape
) -> None:
    helper.release.returns(  # type: ignore[attr-defined]
        admin_pb2.Release(
            id="r2",
            workers=[
                admin_pb2.Worker(index=0, group="default", state="ready"),
                admin_pb2.Worker(index=1, group="default", state="ready"),
            ],
        )
    )
    helper.restart_worker.returns(admin_pb2.WorkerDebug(ok=True))  # type: ignore[attr-defined]
    client.force_login(member)

    response = client.post("/sites/alice/blog/restart/", follow=True)

    assert "Restarted 2 workers of release r2." in response.text
    tape.assert_order(
        tape.where(label="HelperClient.restart_worker").with_args(index=0),
        tape.where(label="HelperClient.restart_worker").with_args(index=1),
    )


def test_a_restart_stops_at_a_worker_that_refuses(
    client: Client, served: Site, helper: HelperClient, member: User, tape: Tape
) -> None:
    helper.release.returns(  # type: ignore[attr-defined]
        admin_pb2.Release(
            id="r2",
            workers=[
                admin_pb2.Worker(index=0, group="default", state="ready"),
                admin_pb2.Worker(index=1, group="default", state="ready"),
            ],
        )
    )
    helper.restart_worker.returns(  # type: ignore[attr-defined]
        admin_pb2.WorkerDebug(ok=False, error="a debugger is attached")
    )
    client.force_login(member)

    response = client.post("/sites/alice/blog/restart/", follow=True)

    assert "Restarted 0 of 2 workers, then one refused: a debugger is attached" in response.text
    tape.where(label="HelperClient.restart_worker").assert_once()


def test_maintenance_is_turned_on_and_shown(
    client: Client, served: Site, helper: HelperClient, member: User, tape: Tape
) -> None:
    helper.set_maintenance.returns(admin_pb2.MaintenanceStatus(on=True))  # type: ignore[attr-defined]
    client.force_login(member)

    response = client.post("/sites/alice/blog/maintenance/", {"on": "1"}, follow=True)

    assert "The maintenance page is on." in response.text
    tape.where(label="HelperClient.set_maintenance").with_args(on=True).assert_once()

    helper.app.returns(  # type: ignore[attr-defined]
        admin_pb2.App(name="site", current_release="r2", maintenance=True)
    )
    page = client.get("/sites/alice/blog/").text

    assert "Maintenance page on" in page
    assert "Turn maintenance off" in page


def test_an_action_the_daemon_refuses_is_shown_and_recorded_as_failed(
    client: Client, served: Site, helper: HelperClient, member: User
) -> None:
    helper.rollback.raises(HelperError("rolling back", Unreachable()))  # type: ignore[attr-defined]
    client.force_login(member)

    response = client.post("/sites/alice/blog/roll-back/", follow=True)

    assert "Rolling back: failed to connect to all addresses." in response.text

    entry = AuditEntry.objects.get(action="roll-back")

    assert entry.succeeded is False


def test_an_action_on_a_site_someone_may_not_see_is_not_found(
    client: Client, served: Site, helper: HelperClient, tape: Tape
) -> None:
    client.force_login(User.objects.create_user("bob", password="correct horse"))

    assert client.post("/sites/alice/blog/roll-back/").status_code == 404
    tape.where(label="HelperClient.rollback").assert_never()


def test_an_action_is_refused_to_someone_who_may_only_look(
    client: Client, served: Site, helper: HelperClient, member: User, tape: Tape
) -> None:
    # Nobody can yet see a site without being able to act on it, so stand in
    # for the rule that will tell the two apart.

    client.force_login(member)

    with wrapture.binding(services, attr="may_operate").overrides(lambda user, site: False):
        assert client.post("/sites/alice/blog/roll-back/").status_code == 403
        assert "Roll back" not in client.get("/sites/alice/blog/").text

    tape.where(label="HelperClient.rollback").assert_never()


def test_actions_are_not_taken_by_a_get(client: Client, served: Site, member: User) -> None:
    client.force_login(member)

    assert client.get("/sites/alice/blog/roll-back/").status_code == 405


def test_deploying_a_directory_from_the_page_queues_a_deploy(
    client: Client,
    served: Site,
    helper: HelperClient,
    member: User,
    tmp_path: Path,
    django_capture_on_commit_callbacks: object,
) -> None:
    helper.plan_deploy.returns(admin_pb2.DeployPlan(release="r3"))  # type: ignore[attr-defined]
    helper.wait_release.returns(admin_pb2.Release(id="r3", state="ready", serving=True))  # type: ignore[attr-defined]
    (tmp_path / "pyproject.toml").write_text("[tool.muru]\n")
    client.force_login(member)

    with django_capture_on_commit_callbacks(execute=True):  # type: ignore[operator]
        response = client.post("/sites/alice/blog/deploy/", {"path": str(tmp_path)}, follow=True)

    assert f"Queued a deploy of {tmp_path}." in response.text

    deploy = served.deploys.first()

    assert deploy is not None
    assert (deploy.release, deploy.state) == ("r3", Deploy.State.SERVING)
    assert AuditEntry.objects.get(action="deploy").actor == member


def test_deploying_a_directory_that_is_not_there_is_refused(
    client: Client, served: Site, member: User
) -> None:
    client.force_login(member)

    response = client.post("/sites/alice/blog/deploy/", {"path": "/no/such/place"}, follow=True)

    assert "/no/such/place is not a directory." in response.text
    assert served.deploys.count() == 1


def test_a_page_deploys_no_directory_where_the_hub_does_not_hold_its_accounts(
    served: Site, member: User, tmp_path: Path, settings: object
) -> None:
    settings.HUB_DEPLOY_FROM_DISK = False  # type: ignore[attr-defined]

    with pytest.raises(services.ActionRefused, match="does not deploy directories"):
        services.deploy_directory(served, tmp_path, member)


def test_the_hello_site_is_deployed_again_from_the_page(
    client: Client,
    served: Site,
    member: User,
    django_capture_on_commit_callbacks: object,
) -> None:
    client.force_login(member)

    with django_capture_on_commit_callbacks(execute=True):  # type: ignore[operator]
        response = client.post("/sites/alice/blog/deploy/", {"source": "hello"}, follow=True)

    assert "Queued a deploy of the hello site." in response.text
    assert served.deploys.count() == 2


def test_the_page_shows_the_log_and_the_events(
    client: Client, served: Site, helper: HelperClient, member: User
) -> None:
    helper.log.returns(["worker 0 is ready", "GET / 200 <b>"])  # type: ignore[attr-defined]
    helper.events.returns(  # type: ignore[attr-defined]
        [
            admin_pb2.Event(
                sequence=2,
                time_unix_ms=1795326180639,
                type="traffic.switched",
                subject="site@r2",
                level="notice",
                message="traffic moved to the release",
            )
        ]
    )
    client.force_login(member)

    page = client.get("/sites/alice/blog/").text

    assert "worker 0 is ready\nGET / 200 &lt;b&gt;" in page
    assert "<code>traffic.switched</code>" in page
    assert "traffic moved to the release" in page


def test_the_live_part_of_the_page_is_served_alone_and_says_when_a_deploy_is_under_way(
    client: Client, served: Site, member: User
) -> None:
    client.force_login(member)

    idle = client.get("/sites/alice/blog/live/").text

    assert "<html" not in idle
    assert 'data-busy="0"' in idle

    Deploy.objects.create(site=served, source_name="x", archive="x", sha256="0" * 64)

    assert 'data-busy="1"' in client.get("/sites/alice/blog/live/").text


def test_the_live_part_of_a_site_someone_may_not_see_is_not_found(
    client: Client, served: Site
) -> None:
    client.force_login(User.objects.create_user("bob", password="correct horse"))

    assert client.get("/sites/alice/blog/live/").status_code == 404
