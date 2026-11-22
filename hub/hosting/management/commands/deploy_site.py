"""Deploy a directory on the hub's machine to a site."""

from pathlib import Path
from typing import Any

from django.core.management.base import BaseCommand, CommandError, CommandParser

from hub.hosting import services


class Command(BaseCommand):
    """Archive a directory and deploy it to a site, as a commit from GitHub would be."""

    help = (
        "Deploy a directory to a site, as OWNER/NAME PATH. The commit is recorded when the "
        "directory is a git checkout with no uncommitted changes."
    )

    def add_arguments(self, parser: CommandParser) -> None:
        """Take the site and the directory."""

        parser.add_argument("site", help="The site, as OWNER/NAME")
        parser.add_argument("path", type=Path, help="The project's directory")

    def handle(self, *args: Any, **options: Any) -> None:
        """Queue the deploy, or say why not."""

        try:
            site = services.find_site(options["site"])
            deploy = services.deploy_directory(site, options["path"].resolve())
        except services.ActionRefused as refused:
            raise CommandError(str(refused)) from None

        commit = f" at commit {deploy.commit[:12]}" if deploy.commit else ""
        self.stdout.write(
            f"queued a deploy of {options['path']}{commit} to {site.slug}; "
            "the jobs worker carries it out"
        )
