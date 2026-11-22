"""The hub's actions on sites.

Pages and management commands, and later the Actions API and the MCP
server, all act through this module, so that who may do what is decided in
one place (specification sections 5.4 and 10.1) and every action is traced
the same way (section 14.2).
"""

from __future__ import annotations

import time
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path

import wrapture
from django.conf import settings
from django.db import transaction
from django.db.models import QuerySet
from django.urls import reverse
from muruhosting_stubs.muru.admin.v1 import admin_pb2

from hub.accounts.models import User
from hub.hosting import tasks
from hub.hosting.archives import Archive, archive_directory
from hub.hosting.helper import HelperClient, HelperError
from hub.hosting.models import APP, AuditEntry, Deploy, Site
from hub.tracing import observed


class ActionRefused(Exception):
    """An action the hub will not take, with the reason to show the person."""


@observed(label="sites.visible_to")
def sites_visible_to(user: User) -> QuerySet[Site]:
    """List the sites a person may see: every site for a platform admin, else their own."""

    sites = Site.objects.select_related("owner")

    if user.is_platform_admin:
        return sites

    return sites.filter(owner=user)


def may_operate(user: User, site: Site) -> bool:
    """Say whether a person may act on a site: deploy to it, roll it back and the rest.

    Until sites have members and viewers of their own (specification section
    5.4), that is the site's owner and a platform admin, who are also the
    people who see it.
    """

    return user.is_platform_admin or site.owner_id == user.pk


def find_site(slug: str) -> Site:
    """Find a site by its OWNER/NAME, or refuse with why not."""

    owner, _, name = slug.partition("/")

    try:
        return Site.objects.select_related("owner").get(owner__username=owner, name=name)
    except Site.DoesNotExist:
        raise ActionRefused(f"There is no site {slug}.") from None


@observed(label="sites.register_local", capture="none")
def register_local_site(
    owner: User, name: str, helper_address: str, token: str, url: str, site_dir: str
) -> Site:
    """Record a site that runs on this machine, and deploy the hello site to it.

    The site's daemon and helper are already running (specification section
    15.3): the hub starts nothing, and deploys the hello site through the
    helper as it does for any new site.
    """

    if Site.objects.filter(owner=owner, name=name).exists():
        raise ActionRefused(f"The site {owner.username}/{name} already exists.")

    site = Site(
        owner=owner,
        name=name,
        kind=Site.Kind.LOCAL,
        state=Site.State.CREATING,
        state_message="Deploying the hello site.",
        url=url,
        helper_address=helper_address,
        helper_token=token,
        site_dir=site_dir,
    )
    site.full_clean()

    with transaction.atomic():
        site.save()
        deploy_hello(site)

    return site


def deploy_hello(site: Site) -> Deploy:
    """Deploy the hello site, telling it which site it is and where its page in the hub is."""

    page = settings.HUB_URL.rstrip("/") + reverse("site", args=[site.owner.username, site.name])

    return start_deploy(
        site,
        archive_directory(settings.HELLO_SITE_DIR),
        prefix="hello",
        description="The hello site",
        env={"HELLO_SITE": site.slug, "HELLO_HUB_URL": page},
    )


@observed(label="sites.redeploy_hello")
def redeploy_hello(site: Site, actor: User | None = None) -> Deploy:
    """Deploy the hello site to a site again, as a new release."""

    deploy = deploy_hello(site)
    _record(site, actor, "deploy", "The hello site", "Queued.")

    return deploy


@observed(label="sites.deploy_directory", capture="none")
def deploy_directory(
    site: Site, directory: Path, actor: User | None = None, hold: bool = False
) -> Deploy:
    """Deploy a directory on the hub's machine to a site.

    With `hold` the release is started and traffic is left where it is, for
    a canary or for someone to serve it when they choose.

    A person may ask for this only where the hub holds its own accounts, on
    a developer's machine: anywhere else it would hand them every directory
    the hub can read.
    """

    if actor is not None and not settings.HUB_DEPLOY_FROM_DISK:
        raise ActionRefused("This hub does not deploy directories of its own machine.")

    if not directory.is_absolute():
        raise ActionRefused("Give the directory as an absolute path.")

    if not directory.is_dir():
        raise ActionRefused(f"{directory} is not a directory.")

    archive = archive_directory(directory)

    deploy = start_deploy(
        site,
        archive,
        prefix=archive.commit[:12] or "local",
        description=f"From {directory}",
        hold=hold,
    )
    _record(site, actor, "deploy", f"From {directory}", "Queued, held." if hold else "Queued.")

    return deploy


def start_deploy(
    site: Site,
    archive: Archive,
    *,
    prefix: str,
    description: str,
    env: dict[str, str] | None = None,
    hold: bool = False,
) -> Deploy:
    """Keep a source archive, record a deploy of it and queue the job that carries it out."""

    # The archive is kept in the hub's data directory, named for its digest,
    # until the job sends it to the site.

    directory: Path = settings.DATA_DIR / "archives"
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / f"{archive.sha256}.tar.gz"
    path.write_bytes(archive.data)

    # A source's directory at the site is named for what it holds, so the
    # same files deployed twice share one directory.

    name = prefix if prefix == archive.commit[:12] else f"{prefix}-{archive.sha256[:12]}"

    deploy = Deploy.objects.create(
        site=site,
        source_name=name,
        archive=path.name,
        sha256=archive.sha256,
        commit=archive.commit,
        description=description,
        env=env or {},
        hold=hold,
        trace_headers=dict(wrapture.trace_headers()),
    )

    # Queue the job once the deploy is committed, so the worker finds it.

    transaction.on_commit(lambda: tasks.run_deploy.enqueue(deploy.pk))

    return deploy


@observed(label="sites.forget")
def forget_site(site: Site) -> None:
    """Forget a site that runs on this machine, leaving its daemon as it is."""

    if site.kind != Site.Kind.LOCAL:
        raise ActionRefused(f"{site.slug} does not run on this machine, so it cannot be forgotten.")

    site.delete()


def _record(
    site: Site, actor: User | None, action: str, detail: str, message: str, succeeded: bool = True
) -> None:
    """Add an action to the audit log."""

    AuditEntry.objects.create(
        site=site,
        actor=actor,
        via=AuditEntry.Via.PAGE if actor is not None else AuditEntry.Via.COMMAND,
        action=action,
        detail=detail[:255],
        message=message,
        succeeded=succeeded,
    )


def _operate(
    site: Site,
    actor: User | None,
    action: str,
    detail: str,
    call: Callable[[HelperClient], str],
) -> str:
    """Make one call to a site's daemon for a person, record it, and return what came of it.

    A call the daemon refuses, or a daemon that does not answer, is recorded
    as a failure and refused with what it said.
    """

    if not site.helper_address:
        raise ActionRefused("The site has no helper to ask.")

    try:
        with HelperClient(site.helper_address, site.helper_token) as helper:
            message = call(helper)
    except HelperError as error:
        _record(site, actor, action, detail, str(error), succeeded=False)

        raise ActionRefused(f"{str(error)[:1].upper()}{str(error)[1:]}.") from error

    _record(site, actor, action, detail, message)

    return message


@observed(label="sites.roll_back")
def roll_back(site: Site, actor: User | None = None) -> str:
    """Move a site's traffic back to the release that served before."""

    def call(helper: HelperClient) -> str:
        return f"Traffic is going back to release {helper.rollback().id}."

    return _operate(site, actor, "roll-back", "", call)


@observed(label="sites.promote")
def promote(site: Site, release: str, actor: User | None = None) -> str:
    """Move a site's traffic to one of its releases."""

    def call(helper: HelperClient) -> str:
        return f"Traffic is going to release {helper.promote(release).id}."

    return _operate(site, actor, "promote", release, call)


# How long a restarted worker's replacement gets to serve before the restart
# gives up on the rest, and how often it is looked at.

RESTART_WAIT = 60.0
RESTART_POLL = 0.25


@observed(label="sites.restart")
def restart(site: Site, actor: User | None = None) -> str:
    """Restart the workers of a site's serving release, one at a time so capacity holds.

    The admin API restarts one worker per call, so the turn-taking is done
    here: each worker is replaced, and the next waits until that replacement
    serves (muruhq/muru#871; #39 here).
    """

    def call(helper: HelperClient) -> str:
        app = helper.app()
        release = helper.release(app.current_release) if app and app.current_release else None

        if release is None:
            return "No release is serving, so there is nothing to restart."

        workers = [(worker.group, worker.index) for worker in release.workers]

        for done, (group, index) in enumerate(workers):
            answer = helper.restart_worker(release.id, group, index)

            if not answer.ok:
                return (
                    f"Restarted {done} of {len(workers)} workers, then one refused: {answer.error}"
                )

            if not _wait_for_workers(helper, release.id):
                return (
                    f"Restarted {done + 1} of {len(workers)} workers; its replacement was "
                    "not serving in time, so the rest were left as they were."
                )

        plural = "" if len(workers) == 1 else "s"

        return f"Restarted {len(workers)} worker{plural} of release {release.id}."

    return _operate(site, actor, "restart", "", call)


def _wait_for_workers(helper: HelperClient, release: str) -> bool:
    """Wait until every worker of a release is ready, and say whether they were in time."""

    deadline = time.monotonic() + RESTART_WAIT

    while time.monotonic() < deadline:
        found = helper.release(release)

        if found is not None and all(worker.state == "ready" for worker in found.workers):
            return True

        time.sleep(RESTART_POLL)

    return False


@observed(label="sites.set_maintenance")
def set_maintenance(site: Site, on: bool, actor: User | None = None) -> str:
    """Turn a site's maintenance page on or off."""

    def call(helper: HelperClient) -> str:
        helper.set_maintenance(on)

        return f"The maintenance page is {'on' if on else 'off'}."

    return _operate(site, actor, "maintenance", "on" if on else "off", call)


# What a canary's steps may be, and how long each may hold.

MAX_STEPS = 10
MIN_HOLD_SECONDS, MAX_HOLD_SECONDS = 5, 3600

ROLLOUT_ACTIONS = {
    "pause": "The rollout is paused at {percent}%.",
    "resume": "The rollout goes on from {percent}%.",
    "promote": "The rollout is promoted: release {candidate} takes all the traffic.",
    "abort": "The rollout is aborted: release {candidate} is out of traffic.",
}


def parse_steps(text: str) -> list[int]:
    """Read a canary's steps, as percentages that rise, or refuse with why not."""

    try:
        steps = [int(part) for part in text.replace(" ", "").split(",") if part]
    except ValueError:
        raise ActionRefused("Give the steps as percentages, such as 10,50.") from None

    if not steps or len(steps) > MAX_STEPS:
        raise ActionRefused(f"Give between 1 and {MAX_STEPS} steps.")

    if any(not 1 <= step <= 100 for step in steps) or steps != sorted(set(steps)):
        raise ActionRefused("Each step is a percentage from 1 to 100, larger than the one before.")

    return steps


@observed(label="sites.start_rollout")
def start_rollout(
    site: Site,
    release: str,
    steps: str,
    hold_seconds: int,
    min_requests: int,
    actor: User | None = None,
) -> str:
    """Start a canary: a held release takes a rising share of a site's requests, step by step."""

    shares = parse_steps(steps)

    if not MIN_HOLD_SECONDS <= hold_seconds <= MAX_HOLD_SECONDS:
        raise ActionRefused(
            f"Each step holds for between {MIN_HOLD_SECONDS} and {MAX_HOLD_SECONDS} seconds."
        )

    if not 1 <= min_requests <= 100_000:
        raise ActionRefused("Give how many requests a step needs before it is judged.")

    def call(helper: HelperClient) -> str:
        rollout = helper.start_rollout(release, shares, hold_seconds, min_requests)

        return (
            f"A canary of release {rollout.candidate} has started against {rollout.baseline}, "
            f"at {shares[0]}%."
        )

    detail = f"{release}: {','.join(map(str, shares))}% for {hold_seconds}s"

    return _operate(site, actor, "rollout-start", detail, call)


@observed(label="sites.control_rollout")
def control_rollout(site: Site, action: str, actor: User | None = None) -> str:
    """Pause, resume, promote or abort a site's rollout."""

    if action not in ROLLOUT_ACTIONS:
        raise ActionRefused(f"A rollout cannot be asked to {action}.")

    def call(helper: HelperClient) -> str:
        rollout = helper.control_rollout(action)

        return ROLLOUT_ACTIONS[action].format(percent=rollout.percent, candidate=rollout.candidate)

    return _operate(site, actor, f"rollout-{action}", "", call)


@observed(label="sites.run_command", capture="none")
def run_command(site: Site, name: str, inputs: dict[str, str], actor: User | None = None) -> int:
    """Run one of the commands a site's serving release declares, and return the run's id.

    Only a declared command is run, with its declared inputs alone. The
    audit entry names the inputs given and shows the values of those that
    are not secret.
    """

    ran = 0

    def call(helper: HelperClient) -> str:
        nonlocal ran

        declared = {command.name: command for command in helper.commands()}

        if name not in declared:
            raise ActionRefused(f"The serving release declares no command {name}.")

        known = {item.name: item for item in declared[name].inputs}
        unknown = sorted(set(inputs) - set(known))

        if unknown:
            raise ActionRefused(f"{name} takes no input {unknown[0]}.")

        missing = [
            item.name for item in known.values() if item.required and not inputs.get(item.name)
        ]

        if missing:
            raise ActionRefused(f"{name} needs a value for {missing[0]}.")

        # An input left empty takes the command's own default.

        given = {key: value for key, value in inputs.items() if value}
        ran = helper.run_command(name, given)

        return f"Started as run {ran}."

    secret = _secret_inputs(site, name)
    shown = ", ".join(
        f"{key}={'***' if key in secret else value}"
        for key, value in sorted(inputs.items())
        if value
    )

    _operate(site, actor, "command-run", f"{name} {shown}".strip(), call)

    return ran


def _secret_inputs(site: Site, name: str) -> set[str]:
    """Name the inputs of a command whose values are never shown or recorded.

    When the daemon cannot say, every input is treated as secret.
    """

    try:
        with HelperClient(site.helper_address, site.helper_token) as helper:
            commands = helper.commands()
    except HelperError:
        return _Everything()

    return {
        item.name
        for command in commands
        if command.name == name
        for item in command.inputs
        if item.secret
    }


class _Everything(set[str]):
    """A set that every name is in."""

    def __contains__(self, name: object) -> bool:
        return True


@observed(label="sites.stop_command_run")
def stop_command_run(site: Site, run: int, actor: User | None = None) -> str:
    """Stop a run of a site's command that is under way."""

    def call(helper: HelperClient) -> str:
        record = helper.command_run(run)

        if record is None or record.app != APP:
            raise ActionRefused(f"The site has no run {run}.")

        helper.stop_command_run(run)

        return f"Run {run} of {record.name} is being stopped."

    return _operate(site, actor, "command-stop", str(run), call)


@dataclass(frozen=True)
class CommandRun:
    """One run of a site's command, with the end of what it wrote."""

    record: admin_pb2.CommandRunRecord
    output: list[str]


# How much of a run's output its page is loaded with.

RUN_LINES_SHOWN = 500


@observed(label="sites.command_run")
def command_run(site: Site, run: int) -> CommandRun | None:
    """Find a run of one of a site's commands, or None when the site has no such run."""

    if not site.helper_address:
        return None

    try:
        with HelperClient(site.helper_address, site.helper_token) as helper:
            record = helper.command_run(run)

            # A run's id is the daemon's, so make sure it is this site's
            # application's before showing it.

            if record is None or record.app != APP:
                return None

            return CommandRun(record=record, output=helper.command_output(run, RUN_LINES_SHOWN))
    except HelperError as error:
        raise ActionRefused(str(error)) from error


@dataclass(frozen=True)
class LiveSite:
    """What a site's daemon says of it now, or why it could not be asked."""

    releases: list[admin_pb2.Release]
    muru_version: str = ""
    error: str = ""
    current_release: str = ""
    previous_release: str = ""
    maintenance: bool = False
    events: list[admin_pb2.Event] = field(default_factory=list)
    log: list[str] = field(default_factory=list)
    rollout: admin_pb2.Rollout | None = None
    commands: list[admin_pb2.CommandInfo] = field(default_factory=list)
    command_runs: list[admin_pb2.CommandRunRecord] = field(default_factory=list)


# How much of a site's events, log and command runs its page shows.

EVENTS_SHOWN = 30
LOG_LINES_SHOWN = 100
RUNS_SHOWN = 10


@observed(label="sites.live")
def live_site(site: Site, feed: bool = True) -> LiveSite:
    """Ask a site's daemon for its releases, newest first, and with `feed` its events and log."""

    if not site.helper_address:
        return LiveSite(releases=[], error="The site has no helper to ask.")

    try:
        with HelperClient(site.helper_address, site.helper_token) as helper:
            status = helper.status()
            releases = helper.releases()
            app = helper.app()
            serving = app is not None and bool(app.current_release)
            events = helper.events(EVENTS_SHOWN) if feed else []
            log = helper.log(LOG_LINES_SHOWN) if feed and serving else []
            rollout = helper.rollout() if app is not None else None
            commands = helper.commands() if serving else []
            runs = helper.command_runs()[:RUNS_SHOWN] if app is not None else []
    except HelperError as error:
        return LiveSite(releases=[], error=str(error))

    releases.sort(key=lambda release: release.created_unix_ms, reverse=True)

    return LiveSite(
        releases=releases,
        muru_version=status.version,
        current_release=app.current_release if app is not None else "",
        previous_release=app.previous_release if app is not None else "",
        maintenance=app.maintenance if app is not None else False,
        events=events,
        log=log,
        rollout=rollout,
        commands=commands,
        command_runs=runs,
    )
