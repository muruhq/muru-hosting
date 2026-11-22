#!/usr/bin/env python

"""Django's command line for the hub."""

import os
import sys


def main() -> None:
    """Run a management command with the hub's settings."""

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hub.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
