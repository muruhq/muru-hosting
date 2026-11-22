"""The hub's actions on sites.

Pages and management commands, and later the Actions API and the MCP
server, all act through this module, so that who may do what is decided in
one place (specification sections 5.4 and 10.1) and every action is traced
the same way (section 14.2).
"""

from __future__ import annotations

from dataclasses import dataclass
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
from hub.hosting.models import Deploy, Site
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


@observed(label="sites.deploy_directory", capture="none")
def deploy_directory(site: Site, directory: Path) -> Deploy:
    """Deploy a directory on the hub's machine to a site."""

    if not directory.is_dir():
        raise ActionRefused(f"{directory} is not a directory.")

    archive = archive_directory(directory)

    return start_deploy(
        site,
        archive,
        prefix=archive.commit[:12] or "local",
        description=f"From {directory}",
    )


def start_deploy(
    site: Site,
    archive: Archive,
    *,
    prefix: str,
    description: str,
    env: dict[str, str] | None = None,
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


@dataclass(frozen=True)
class LiveSite:
    """What a site's daemon says of it now, or why it could not be asked."""

    releases: list[admin_pb2.Release]
    muru_version: str = ""
    error: str = ""


@observed(label="sites.live")
def live_site(site: Site) -> LiveSite:
    """Ask a site's daemon for its releases, newest first."""

    if not site.helper_address:
        return LiveSite(releases=[], error="The site has no helper to ask.")

    try:
        with HelperClient(site.helper_address, site.helper_token) as helper:
            status = helper.status()
            releases = helper.releases()
    except HelperError as error:
        return LiveSite(releases=[], error=str(error))

    releases.sort(key=lambda release: release.created_unix_ms, reverse=True)

    return LiveSite(releases=releases, muru_version=status.version)
