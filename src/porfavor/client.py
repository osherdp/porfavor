"""Publish documentation for a project on the server.

Usage:
    client.py <host> <project> <directory>
    client.py -h | --help

Options:
    -h --help           Display help message and exit.
"""
# pylint: disable=no-value-for-parameter
from __future__ import print_function
from __future__ import absolute_import

import os
import shutil
import tempfile

import click
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder


def publish(host, project, root_dir):
    """Deploy documentation on the server.

    Args:
        host (str): URL for reaching the server, e.g.: "docs:5000/".
        project (str): the project's name.
        root_dir (str): path to the root directory containing the
            documentation (should include a "index.html" file and such).
    """
    temp_dir = None
    try:
        temp_dir = tempfile.mkdtemp()
        click.secho("Zipping content of folder '{}'... ".format(root_dir),
                    nl=False)
        shutil.make_archive(os.path.join(temp_dir, project), "zip", root_dir)
        click.secho("DONE!", bold=True, fg="green")

        click.secho("Publishing content for project '{}'... ".format(project),
                    nl=False)
        filename = "{}.zip".format(project)
        with open(os.path.join(temp_dir, filename), "rb") as zip_file:
            content = zip_file.read()

        multipart = MultipartEncoder(
            fields={"files": (filename, content, "text/plain")}
        )

        response = requests.put(
            "http://{}/api/upload_docs".format(host),
            data=multipart,
            headers={"Content-Type": multipart.content_type})

        response.raise_for_status()
        click.secho("DONE!", bold=True, fg="green")

    finally:
        if temp_dir is not None:
            shutil.rmtree(temp_dir)


@click.command("publish",
               short_help="Send documentation to the server.",
               context_settings=dict(help_option_names=['-h', '--help']))
@click.argument("host", metavar="<host>")
@click.argument("project", metavar="<project>")
@click.argument("directory", metavar="<directory>",
                type=click.Path(exists=True, file_okay=False))
def publish_cli(host, project, directory):
    """Publish documentation for a project on the server."""
    publish(host=host,
            project=project,
            root_dir=directory)


if __name__ == "__main__":
    publish_cli()
