"""Run the hosting documentation server.

Usage:
    server.py [--work-dir <dir>] [-p <port> | --port <port>] [-D | --daemon]
    server.py -h | --help

Options:
    -h --help                   Display help message and exit.
    --work-dir <dir>            Directory to server files under it [Default: .]
    --port <port> -p <port>     Port for the web server [Default: 5000].
    -D --daemon                 Run in the background.
"""
from __future__ import print_function
import os
import threading

import docopt
from rpyc import Service
from rpyc.utils.helpers import classpartial
from rpyc.utils.server import ThreadedServer
from flask import Flask, render_template, abort, send_file


class PublishService(Service):
    def __init__(self, work_dir):
        self.work_dir = work_dir

    def exposed_publish(self, project, project_docs):
        for relative_path, content in project_docs:
            path = os.path.join(self.work_dir,
                                project,
                                relative_path)
            directory = os.path.dirname(path)

            if not os.path.isdir(directory):
                os.makedirs(directory)

            with open(path, "wb") as f:
                f.write(content)


def run_server(work_dir, port, daemon):
    work_dir = os.path.abspath(work_dir)
    app = Flask(__name__)

    @app.route('/')
    def index():
        projects = [filename for filename in os.listdir(work_dir)
                    if os.path.isdir(os.path.join(work_dir, filename))]

        return render_template("index.html",
                               projects=projects)

    @app.route('/<path:path>')
    def static_proxy(path):
        path = path.replace("/", os.sep)
        path = os.path.join(work_dir, path)
        directory, filename = os.path.split(path)
        if not path.startswith(directory):
            abort(401)

        return send_file(path)

    publish_server = ThreadedServer(classpartial(PublishService, work_dir),
                                    port=12341)
    thread = threading.Thread(target=publish_server.start)
    thread.daemon = True
    thread.start()

    app.run(port=port)


def main():
    arguments = docopt.docopt(__doc__)
    run_server(work_dir=arguments["--work-dir"],
               port=int(arguments["--port"]),
               daemon=arguments["--daemon"])


if __name__ == "__main__":
    main()
