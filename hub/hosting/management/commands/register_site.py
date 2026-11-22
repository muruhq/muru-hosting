"""Record a site that runs on this machine with the hub."""

from pathlib import Path
from typing import Any

from django.core.management.base import BaseCommand, CommandError, CommandParser

from hub.accounts.models import User
from hub.hosting import services


class Command(BaseCommand):
    """Record a local site's helper with the hub, which then deploys the hello site to it."""

    help = (
        "Record a site whose daemon and helper run on this machine, as OWNER/NAME. "
        "The hub deploys the hello site to it through the helper."
    )

    def add_arguments(self, parser: CommandParser) -> None:
        """Take the site, its helper's address and token, and where the site answers."""

        parser.add_argument("site", help="The site, as OWNER/NAME; the owner's account must exist")
        parser.add_argument("--helper", required=True, help="The helper's address, as HOST:PORT")
        parser.add_argument("--token-file", required=True, help="A file holding the helper's token")
        parser.add_argument(
            "--site-dir", required=True, help="The site's directory, as its daemon reads it"
        )
        parser.add_argument("--url", required=True, help="Where the site answers")

    def handle(self, *args: Any, **options: Any) -> None:
        """Register the site, or say why not."""

        username, _, name = options["site"].partition("/")

        try:
            owner = User.objects.get(username=username)
        except User.DoesNotExist:
            raise CommandError(
                f"There is no account {username}. Make it first, with createsuperuser "
                "or in the admin site."
            ) from None

        token = Path(options["token_file"]).read_text().strip()

        try:
            site = services.register_local_site(
                owner, name, options["helper"], token, options["url"], options["site_dir"]
            )
        except services.ActionRefused as refused:
            raise CommandError(str(refused)) from None

        self.stdout.write(f"registered {site.slug}; the hello site is being deployed to it")
