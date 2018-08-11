"""Publish documentation for a project on the server.

Usage:
    client.py <host> <project> <directory>
    client.py -h | --help

Options:
    -h --help           Display help message and exit.
"""
# pylint: disable=no-value-for-parameter
from __future__ import print_function, absolute_import

import os
import shutil
import zipfile
import tempfile

import click
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder


def get_zipped_content(file_or_directory):
    """Return zipped content of given file or directory.

    Args:
        file_or_directory (str): path for the filesystem file or directory to
            be zipped.

    Returns:
        str: bytes of the zip file containing required files.
    """
    if os.path.splitext(file_or_directory)[1] == ".zip":
        click.secho("File iz already zipped... ", nl=False)
        click.secho("SKIP!", bold=True, fg="yellow")
        with open(file_or_directory, "rb") as zipped_file:
            return zipped_file.read()

    click.secho("Zipping content of '{}'... ".format(file_or_directory),
                nl=False)

    temp_dir = None
    try:
        temp_dir = tempfile.mkdtemp()

        zip_path = os.path.join(temp_dir, "content.zip")
        if os.path.isfile(file_or_directory):
            with zipfile.ZipFile(zip_path, mode="w") as zipped_file:
                zipped_file.write(file_or_directory)

        else:
            # make_archive likes getting filename without the extension
            shutil.make_archive(zip_path[:-len(".zip")], "zip",
                                file_or_directory)

        click.secho("DONE!", bold=True, fg="green")
        with open(zip_path, "rb") as zipped_file:
            return zipped_file.read()

    finally:
        if temp_dir is not None:
            shutil.rmtree(temp_dir)


def deploy_documentation(content, host, project):
    """Send documentation content to the server.

    Args:
        content (str): the zipped documentation content.
        host (str): URL for reaching the server, e.g.: "docs:5000/".
        project (str): the project's name.
    """
    click.secho("Publishing content for project '{}'... ".format(project),
                nl=False)

    filename = "{}.zip".format(project)
    multipart = MultipartEncoder(
        fields={"files": (filename, content, "text/plain")}
    )
    response = requests.put(
        "http://{}/api/upload_docs".format(host),
        data=multipart,
        headers={"Content-Type": multipart.content_type})
    response.raise_for_status()

    click.secho("DONE!", bold=True, fg="green")


def publish(host, project, file_or_directory):
    """Deploy documentation on the server.

    Args:
        host (str): URL for reaching the server, e.g.: "docs:5000/".
        project (str): the project's name.
        file_or_directory (str): path to the root directory or file containing
            the documentation, e.g.: "index.html", "path/to/root/dir".
    """
    content = get_zipped_content(file_or_directory)
    deploy_documentation(content, host, project)


@click.command("publish",
               short_help="Send documentation to the server.",
               context_settings=dict(help_option_names=['-h', '--help']))
@click.argument("host", metavar="<host>")
@click.argument("project", metavar="<project>")
@click.argument("file_or_directory", metavar="<file_or_directory>",
                type=click.Path(exists=True))
def publish_cli(host, project, file_or_directory):
    """Publish documentation for a project on the server."""
    publish(host=host,
            project=project,
            file_or_directory=file_or_directory)


if __name__ == "__main__":
    publish_cli()
