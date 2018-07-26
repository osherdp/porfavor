"""Manage documentation in a client-server architecture."""
from __future__ import absolute_import

import click

from .server.main import server_cli
from .client import publish, publish_cli  # noqa


@click.group(context_settings=dict(help_option_names=['-h', '--help']))
def main():
    """Manage documentation the easiest way possible."""


main.add_command(server_cli)
main.add_command(publish_cli)


if __name__ == "__main__":
    main()
