"""Held deploys, canaries and declared commands from a site's pages, with a stand-in helper."""

from pathlib import Path

import pytest
import wrapture
from django.test import Client
from muruhosting_stubs.muru.admin.v1 import admin_pb2
from wrapture import Tape

from hub.accounts.models import User
from hub.hosting import live, services
from hub.hosting.helper import HelperClient
from hub.hosting.models import AuditEntry, Deploy, Site
from tests.test_live import Bridge


@pytest.fixture
def held(site: Site, helper: HelperClient) -> Site:
    """Give the site a release that serves and a newer one started and held."""

    helper.app.returns(admin_pb2.App(name="site", current_release="r1"))  # type: ignore[attr-defined]
    helper.releases.returns(  # type: ignore[attr-defined]
        [
            admin_pb2.Release(id="r2", state="ready", created_unix_ms=2000),
            admin_pb2.Release(id="r1", state="ready", serving=True, created_unix_ms=1000),
        ]
    )

    return site


def rollout(state: str = "running", percent: int = 10) -> admin_pb2.Rollout:
    """Make a canary of r2 against r1, at its first step."""

    return admin_pb2.Rollout(
        id="1",
        candidate="r2",
        baseline="r1",
        state=state,
        percent=percent,
        steps=[admin_pb2.RolloutStep(percent=10), admin_pb2.RolloutStep(percent=50)],
        message="step 1 of 2: 10% for 60s",
    )


def test_a_held_deploy_starts_the_release_without_traffic(
    held: Site,
    helper: HelperClient,
    member: User,
    tmp_path: Path,
    tape: Tape,
    django_capture_on_commit_callbacks: object,
) -> None:
    helper.plan_deploy.returns(admin_pb2.DeployPlan(release="r3"))  # type: ignore[attr-defined]
    helper.wait_release.returns(admin_pb2.Release(id="r3", state="ready"))  # type: ignore[attr-defined]

    with django_capture_on_commit_callbacks(execute=True):  # type: ignore[operator]
        deploy = services.deploy_directory(held, tmp_path, member, hold=True)

    deploy.refresh_from_db()

    assert deploy.state == Deploy.State.HELD
    tape.where(label="HelperClient.deploy").with_args(hold=True).assert_once()


def test_a_held_release_is_offered_a_canary(client: Client, held: Site, member: User) -> None:
    client.force_login(member)

    page = client.get("/sites/alice/blog/").text

    assert 'href="/sites/alice/blog/releases/r2/canary/"' in page
    assert "Start a canary" in client.get("/sites/alice/blog/releases/r2/canary/").text


def test_starting_a_canary_gives_the_daemon_its_steps(
    client: Client, held: Site, helper: HelperClient, member: User, tape: Tape
) -> None:
    helper.start_rollout.returns(rollout())  # type: ignore[attr-defined]
    client.force_login(member)

    response = client.post(
        "/sites/alice/blog/releases/r2/canary/",
        {"steps": "10, 50", "hold": "30", "min_requests": "5"},
        follow=True,
    )

    assert "A canary of release r2 has started against r1, at 10%." in response.text
    tape.where(label="HelperClient.start_rollout").with_args(
        release="r2", steps=[10, 50], hold_seconds=30, min_requests=5
    ).assert_once()
    assert AuditEntry.objects.get(action="rollout-start").detail == "r2: 10,50% for 30s"


@pytest.mark.parametrize("steps", ["", "50,10", "10,10", "0,50", "10,101", "ten"])
def test_steps_that_do_not_rise_are_refused(steps: str) -> None:
    with pytest.raises(services.ActionRefused):
        services.parse_steps(steps)


def test_a_canary_form_that_is_refused_is_shown_again_as_it_was_filled_in(
    client: Client, held: Site, helper: HelperClient, member: User, tape: Tape
) -> None:
    client.force_login(member)

    response = client.post(
        "/sites/alice/blog/releases/r2/canary/",
        {"steps": "50,10", "hold": "30", "min_requests": "5"},
    )

    assert "larger than the one before" in response.text
    assert 'value="50,10"' in response.text
    tape.where(label="HelperClient.start_rollout").assert_never()


def test_a_rollout_under_way_is_shown_with_its_controls(
    client: Client, held: Site, helper: HelperClient, member: User
) -> None:
    helper.rollout.returns(rollout())  # type: ignore[attr-defined]
    client.force_login(member)

    page = client.get("/sites/alice/blog/").text

    assert "Step 1 of 2: release r2 takes 10% of requests." in page
    assert 'action="/sites/alice/blog/rollout/pause/"' in page
    assert 'action="/sites/alice/blog/rollout/abort/"' in page
    assert "Start a canary" not in page


def test_a_rollout_that_has_ended_has_no_controls(
    client: Client, held: Site, helper: HelperClient, member: User
) -> None:
    helper.rollout.returns(rollout("rolled_back", 0))  # type: ignore[attr-defined]
    client.force_login(member)

    page = client.get("/sites/alice/blog/").text

    assert "Rolled back" in page
    assert "/rollout/pause/" not in page


def test_pausing_a_rollout_asks_the_daemon(
    client: Client, held: Site, helper: HelperClient, member: User, tape: Tape
) -> None:
    helper.control_rollout.returns(rollout("paused"))  # type: ignore[attr-defined]
    client.force_login(member)

    response = client.post("/sites/alice/blog/rollout/pause/", follow=True)

    assert "The rollout is paused at 10%." in response.text
    tape.where(label="HelperClient.control_rollout").with_args(action="pause").assert_once()


def test_a_rollout_is_asked_only_what_a_rollout_can_do(
    client: Client, held: Site, helper: HelperClient, member: User, tape: Tape
) -> None:
    client.force_login(member)

    response = client.post("/sites/alice/blog/rollout/explode/", follow=True)

    assert "A rollout cannot be asked to explode." in response.text
    tape.where(label="HelperClient.control_rollout").assert_never()


@pytest.fixture
def commands(site: Site, helper: HelperClient) -> Site:
    """Give the site's serving release two declared commands."""

    helper.commands.returns(  # type: ignore[attr-defined]
        [
            admin_pb2.CommandInfo(
                name="add-user",
                description="Create an account",
                run=["python", "manage.py", "createsuperuser"],
                inputs=[
                    admin_pb2.CommandInputInfo(name="username", required=True),
                    admin_pb2.CommandInputInfo(name="password", required=True, secret=True),
                    admin_pb2.CommandInputInfo(name="email", default="nobody@example.com"),
                ],
            ),
            admin_pb2.CommandInfo(name="migrate", description="Apply migrations"),
        ]
    )
    helper.run_command.returns(7)  # type: ignore[attr-defined]

    return site


def test_the_page_lists_the_commands_the_release_declares(
    client: Client, commands: Site, member: User
) -> None:
    client.force_login(member)

    page = client.get("/sites/alice/blog/").text

    assert "Create an account" in page
    assert 'href="/sites/alice/blog/commands/migrate/"' in page


def test_a_commands_page_asks_for_its_inputs(client: Client, commands: Site, member: User) -> None:
    client.force_login(member)

    page = client.get("/sites/alice/blog/commands/add-user/").text

    assert 'type="password" id="input-password"' in page
    assert 'placeholder="nobody@example.com"' in page
    assert "username (required)" in page


def test_running_a_command_starts_it_and_shows_its_run(
    client: Client, commands: Site, helper: HelperClient, member: User, tape: Tape
) -> None:
    client.force_login(member)

    response = client.post(
        "/sites/alice/blog/commands/add-user/",
        {"input-username": "amy", "input-password": "hunter2", "input-email": ""},
    )

    assert response.headers["Location"] == "/sites/alice/blog/runs/7/"
    tape.where(label="HelperClient.run_command").with_args(
        name="add-user", inputs={"username": "amy", "password": "hunter2"}
    ).assert_once()

    # The audit entry shows what was given, and never a secret's value.

    entry = AuditEntry.objects.get(action="command-run")

    assert entry.detail == "add-user password=***, username=amy"
    assert "hunter2" not in entry.message


def test_a_command_without_a_required_input_is_not_run(
    client: Client, commands: Site, helper: HelperClient, member: User, tape: Tape
) -> None:
    client.force_login(member)

    response = client.post("/sites/alice/blog/commands/add-user/", {"input-username": "amy"})

    assert "add-user needs a value for password." in response.text
    tape.where(label="HelperClient.run_command").assert_never()


def test_a_command_the_release_does_not_declare_is_not_found(
    client: Client, commands: Site, helper: HelperClient, member: User, tape: Tape
) -> None:
    client.force_login(member)

    assert client.post("/sites/alice/blog/commands/shell/").status_code == 404
    tape.where(label="HelperClient.run_command").assert_never()

    with pytest.raises(services.ActionRefused, match="declares no command shell"):
        services.run_command(commands, "shell", {}, member)


def run_record(app: str = "site", under_way: bool = True) -> admin_pb2.CommandRunRecord:
    """Make the daemon's record of run 7."""

    return admin_pb2.CommandRunRecord(
        run=7,
        app=app,
        release="r1",
        name="migrate",
        under_way=under_way,
        ok=not under_way,
        started_unix_ms=1795326180639,
        message="" if under_way else "exited with status 0 after 3s",
    )


def test_a_runs_page_shows_its_output_and_follows_it_while_it_is_under_way(
    client: Client, commands: Site, helper: HelperClient, member: User
) -> None:
    helper.command_run.returns(run_record())  # type: ignore[attr-defined]
    helper.command_output.returns(["applying 0001", "applying <0002>"])  # type: ignore[attr-defined]
    client.force_login(member)

    page = client.get("/sites/alice/blog/runs/7/").text

    assert "applying 0001\napplying &lt;0002&gt;" in page
    assert "Under way" in page
    assert 'data-stream="/sites/alice/blog/runs/7/stream/"' in page
    assert "Stop the run" in page


def test_a_run_that_has_ended_is_not_followed(
    client: Client, commands: Site, helper: HelperClient, member: User
) -> None:
    helper.command_run.returns(run_record(under_way=False))  # type: ignore[attr-defined]
    helper.command_output.returns(["done"])  # type: ignore[attr-defined]
    client.force_login(member)

    page = client.get("/sites/alice/blog/runs/7/").text

    assert "Succeeded" in page
    assert "data-stream" not in page
    assert "Stop the run" not in page


def test_a_run_of_another_application_is_not_shown(
    client: Client, commands: Site, helper: HelperClient, member: User, tape: Tape
) -> None:
    helper.command_run.returns(run_record(app="other"))  # type: ignore[attr-defined]
    client.force_login(member)

    assert client.get("/sites/alice/blog/runs/7/").status_code == 404
    assert client.get("/sites/alice/blog/runs/7/stream/").status_code == 404
    tape.where(label="HelperClient.command_output").assert_never()


def test_a_runs_stream_is_handed_on_with_the_run(
    client: Client, commands: Site, helper: HelperClient, member: User
) -> None:
    helper.command_run.returns(run_record())  # type: ignore[attr-defined]
    helper.command_output.returns([])  # type: ignore[attr-defined]
    bridge = Bridge()
    client.force_login(member)

    response = client.get("/sites/alice/blog/runs/7/stream/", **{"muru.wsgi_to_asgi": bridge})  # type: ignore[arg-type]

    assert response.status_code == 200
    assert bridge.handed_to is live.run_stream
    assert bridge.scope["state"]["run"] == 7


def test_stopping_a_run_asks_the_daemon(
    client: Client, commands: Site, helper: HelperClient, member: User, tape: Tape
) -> None:
    helper.command_run.returns(run_record())  # type: ignore[attr-defined]
    helper.command_output.returns([])  # type: ignore[attr-defined]
    helper.stop_command_run.returns(run_record())  # type: ignore[attr-defined]
    client.force_login(member)

    response = client.post("/sites/alice/blog/runs/7/stop/", follow=True)

    assert "Run 7 of migrate is being stopped." in response.text
    tape.where(label="HelperClient.stop_command_run").with_args(run=7).assert_once()


def test_the_pages_that_act_are_refused_to_someone_who_may_only_look(
    client: Client, commands: Site, member: User
) -> None:
    client.force_login(member)

    with wrapture.binding(services, attr="may_operate").overrides(lambda user, site: False):
        assert client.get("/sites/alice/blog/commands/migrate/").status_code == 403
        assert client.get("/sites/alice/blog/releases/r2/canary/").status_code == 403
        assert client.post("/sites/alice/blog/runs/7/stop/").status_code == 403
        assert client.post("/sites/alice/blog/rollout/abort/").status_code == 403
