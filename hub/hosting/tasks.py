"""The hub's jobs (specification section 2.3).

A job mostly calls a site's helper and waits: the slow parts happen in the
site's daemon. Each job records how far it has got on the row it works on,
so that one run again goes on from the last finished step.
"""

from __future__ import annotations

import json

import wrapture
from django.conf import settings
from django.tasks import task
from django.utils import timezone

from hub.hosting.helper import HelperClient, HelperError
from hub.hosting.models import APP, Deploy, Site

# How long a release gets to build its environment and start.

RELEASE_TIMEOUT = 600.0


class DeployFailed(Exception):
    """A deploy that cannot go on, with the reason to record."""


@task
def run_deploy(deploy_id: int) -> None:
    """Carry out a deploy: upload its source to the site, then deploy and wait for the release."""

    deploy = Deploy.objects.select_related("site", "site__owner").get(pk=deploy_id)
    site = deploy.site

    if deploy.state in {Deploy.State.SERVING, Deploy.State.HELD, Deploy.State.FAILED}:
        return

    # The job joins the trace that asked for the deploy, so the request, the
    # job and its calls to the helper read as one.

    with wrapture.block(
        "job:deploy",
        joins=deploy.trace_headers or None,
        data={"site": site.slug, "deploy": deploy.pk},
    ):
        try:
            with HelperClient(site.helper_address, site.helper_token) as helper:
                _deploy(deploy, helper)
        except (DeployFailed, HelperError) as error:
            _finish(deploy, Deploy.State.FAILED, str(error))
        else:
            _finish(deploy, Deploy.State.HELD if deploy.hold else Deploy.State.SERVING, "")


def _deploy(deploy: Deploy, helper: HelperClient) -> None:
    """Take a deploy through its steps, skipping those an earlier run finished."""

    with wrapture.block("deploy:health"):
        helper.status()

    # A site being created is given its application's settings before its
    # first release: the data directory on the site's own directory, where
    # it outlives the daemon's state (specification section 3.2). It is
    # applied here because the daemon's own file does not take it
    # (muruhq/muru#862; #32 here).

    site = deploy.site

    if site.state == Site.State.CREATING and site.site_dir:
        with wrapture.block("deploy:configure"):
            report = helper.apply_config(site_config(site))

            if report.errors:
                raise DeployFailed("; ".join(report.errors))

    if not deploy.source_path:
        with wrapture.block("deploy:upload"):
            _set(deploy, state=Deploy.State.UPLOADING)
            archive = (settings.DATA_DIR / "archives" / deploy.archive).read_bytes()
            path = helper.upload_source(deploy.source_name, deploy.sha256, deploy.commit, archive)
            _set(deploy, source_path=path)

    # The release's id is settled, and recorded, before the release is
    # made, so that a job run again knows which release is its own.

    if not deploy.release:
        with wrapture.block("deploy:plan"):
            plan = helper.plan_deploy(deploy.source_path, deploy.env, deploy.hold)

            if plan.refusals:
                raise DeployFailed("; ".join(plan.refusals))

            _set(deploy, release=plan.release, state=Deploy.State.DEPLOYING)

    with wrapture.block("deploy:release"):
        if helper.release(deploy.release) is None:
            helper.deploy(deploy.source_path, deploy.env, deploy.release, deploy.hold)

    with wrapture.block("deploy:wait"):
        release = helper.wait_release(deploy.release, RELEASE_TIMEOUT)

    if release.state != "ready":
        raise DeployFailed(release.message or f"The release is {release.state}.")


def site_config(site: Site) -> str:
    """Write the declarative document for a site's application."""

    data_dir = json.dumps(f"{site.site_dir.rstrip('/')}/data")

    return f"[app.{APP}]\ndata_dir = {data_dir}\n"


def _set(deploy: Deploy, **fields: str) -> None:
    """Record how far a deploy has got."""

    for name, value in fields.items():
        setattr(deploy, name, value)

    deploy.save(update_fields=list(fields))


def _finish(deploy: Deploy, state: Deploy.State, message: str) -> None:
    """Record how a deploy ended, and what that makes of a site still being created."""

    deploy.state = state
    deploy.message = message
    deploy.finished_at = timezone.now()
    deploy.save(update_fields=["state", "message", "finished_at"])

    site = deploy.site

    if site.state != Site.State.CREATING or state == Deploy.State.HELD:
        return

    if state == Deploy.State.SERVING:
        site.state, site.state_message = Site.State.READY, ""
    else:
        site.state, site.state_message = Site.State.FAILED, message

    site.save(update_fields=["state", "state_message"])
