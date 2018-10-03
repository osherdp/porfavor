"""Run the hosting documentation server.

Usage:
    main.py [WORK_DIR] [-H <host> | --host <host>]
                         [-p <port> | --port <port>]
    main.py -h | --help

Options:
    -h --help                 Display help message and exit.
    --host <host> -H <host>   Host ip address of the server [Default: 0.0.0.0].
    --port <port> -p <port>   Port for the web server [Default: 5000].
"""
# pylint: disable=no-value-for-parameter,no-member
from __future__ import print_function, absolute_import

import os
import http.client

import click
from flask import Flask, render_template, abort, send_file

from .api import api


app = Flask(__name__)  # pylint: disable=invalid-name
app.config["SECRET_KEY"] = (b'\xc0)\xc6\x13\x87b\xb2\xdf\xbd\x8d\t\x9a'
                            b'\x81\x9f\x0e\xa0\xd6\xdd\xce\x95\x91ro\x10')

app.config["UPLOAD_FOLDER"] = os.path.abspath(
    os.environ.get("PORFAVOR_WORKDIR", "."))


app.register_blueprint(api, url_prefix="/api")


@app.route('/')
def index():
    """Display the index page of all projects."""
    work_dir = app.config["UPLOAD_FOLDER"]
    projects = [filename for filename in os.listdir(work_dir)
                if os.path.isdir(os.path.join(work_dir, filename))]

    return render_template("index.html",
                           projects=projects)


@app.route('/static/<path:path>')
def static_serve(path):
    """Serve static files."""
    static_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    "static")

    return send_file(os.path.join(static_directory, path))


@app.route('/projects/<path:path>')
def static_proxy(path):
    """Serve documentation files."""
    work_dir = app.config["UPLOAD_FOLDER"]

    actual_path = os.path.join(work_dir, path)
    directory, _ = os.path.split(actual_path)
    if not actual_path.startswith(directory):
        abort(http.client.UNAUTHORIZED)

    return send_file(os.path.join(work_dir, path))


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
    app.run(host=host, port=port, debug=True)


if __name__ == "__main__":
    server_cli()
