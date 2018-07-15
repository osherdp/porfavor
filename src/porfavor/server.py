"""Run the hosting documentation server.

Usage:
    server.py [WORK_DIR] [-H <host> | --host <host>]
                         [-p <port> | --port <port>]
    server.py -h | --help

Options:
    -h --help                 Display help message and exit.
    --host <host> -H <host>   Host ip address of the server [Default: 0.0.0.0].
    --port <port> -p <port>   Port for the web server [Default: 5000].
"""
# pylint: disable=no-value-for-parameter
from __future__ import print_function
from __future__ import absolute_import

import os
import json
import zipfile

import click
from flask import Flask, render_template, abort, send_file, Response, request


app = Flask(__name__)  # pylint: disable=invalid-name
app.config["SECRET_KEY"] = (b'\xc0)\xc6\x13\x87b\xb2\xdf\xbd\x8d\t\x9a'
                            b'\x81\x9f\x0e\xa0\xd6\xdd\xce\x95\x91ro\x10')

app.config["UPLOAD_FOLDER"] = os.environ.get("PORFAVOR_WORK_DIR")
if app.config["UPLOAD_FOLDER"]:
    app.config["UPLOAD_FOLDER"] = os.path.abspath(app.config["UPLOAD_FOLDER"])


@app.route('/')
def index():
    """Display the index page of all projects."""
    work_dir = app.config["UPLOAD_FOLDER"]
    projects = [filename for filename in os.listdir(work_dir)
                if os.path.isdir(os.path.join(work_dir, filename))]

    return render_template("index.html",
                           projects=projects)


@app.route('/api/get_projects')
def get_projects():
    """Map every project to its info."""
    work_dir = app.config["UPLOAD_FOLDER"]
    projects = {}
    for path in os.listdir(work_dir):
        if os.path.isdir(os.path.join(work_dir, path)):
            icon_path = os.path.join(work_dir, path, "icon.png")
            revealed_icon_path = os.path.join("projects", path, "icon.png")
            projects[path] = {
                "icon":
                    revealed_icon_path if os.path.exists(icon_path) else None
            }

    return Response(json.dumps(projects), mimetype="application/json")


@app.route('/api/upload_docs', methods=["PUT"])
def upload_documentation():
    """Enable deployment of documentation files."""
    if not request.files:
        return "No file was supplied in the request", 400

    for doc_file in request.files.values():
        if doc_file.filename == "":
            return "Documentation file name is empty", 400

        if not doc_file.filename.endswith(".zip"):
            return ("Documentation file {} is "
                    "not a zip file".format(doc_file), 400)

        local_zip_path = os.path.join(app.config["UPLOAD_FOLDER"],
                                      doc_file.filename)
        doc_file.save(local_zip_path)

        with zipfile.ZipFile(local_zip_path) as zip_file:
            destination_dir, _ = os.path.splitext(local_zip_path)
            zip_file.extractall(destination_dir)

    return "", 204


def _serve_static_file_from_directory(base_dir, path):
    """Serve a file."""
    path = os.path.join(base_dir, path)
    return send_file(path)


@app.route('/static/<path:path>')
def static_serve(path):
    """Serve static files."""
    static_directory = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "static")
    return _serve_static_file_from_directory(static_directory, path)


@app.route('/projects/<path:path>')
def static_proxy(path):
    """Serve documentation files."""
    work_dir = app.config["UPLOAD_FOLDER"]

    actual_path = os.path.join(work_dir, path)
    directory, _ = os.path.split(actual_path)
    if not actual_path.startswith(directory):
        abort(401)

    return _serve_static_file_from_directory(work_dir, path)


@click.command("serve",
               short_help="Serve documentation.",
               context_settings=dict(help_option_names=['-h', '--help']))
@click.argument("work_dir", default=".",
                type=click.Path(exists=True, file_okay=False,
                                resolve_path=True))
@click.option("--host", "-H", default="0.0.0.0")
@click.option("--port", "-p", type=int, default=5000)
def server_cli(work_dir, host, port):
    """Run the server side of porfavor.

    Warning: not to be used on production.
    """
    app.config["UPLOAD_FOLDER"] = work_dir
    app.run(host=host, port=port)


if __name__ == "__main__":
    server_cli()
