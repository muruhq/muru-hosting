"""Forget a site that runs on this machine."""

from typing import Any

from django.core.management.base import BaseCommand, CommandError, CommandParser

from hub.hosting import services


class Command(BaseCommand):
    """Remove a local site from the hub, leaving its daemon and helper as they are."""

    help = "Forget a site that runs on this machine, as OWNER/NAME."

    def add_arguments(self, parser: CommandParser) -> None:
        """Take the site."""

        parser.add_argument("site", help="The site, as OWNER/NAME")

    def handle(self, *args: Any, **options: Any) -> None:
        """Forget the site, or say why not."""

        try:
            site = services.find_site(options["site"])
            services.forget_site(site)
        except services.ActionRefused as refused:
            raise CommandError(str(refused)) from None

        self.stdout.write(f"forgot {options['site']}")
