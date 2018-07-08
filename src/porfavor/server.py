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

import json
import os
import threading

import magic
import docopt
from rpyc import Service
from rpyc.utils.helpers import classpartial
from rpyc.utils.server import ThreadedServer
from flask import Flask, send_from_directory, render_template, abort, Response


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
    app = Flask(__name__)

    @app.route('/')
    def index():
        projects = [filename for filename in os.listdir(work_dir)
                    if os.path.isdir(os.path.join(work_dir, filename))]

        return render_template("index.html",
                               projects=projects)


    @app.route('/api/get_projects')
    def get_projects():
        projects = {}
        for path in os.listdir(work_dir):
            if os.path.isdir(os.path.join(work_dir, path)):
                icon_path = os.path.join(work_dir, path, "icon.png")
                projects[path] = {
                    "icon": icon_path if os.path.exists(icon_path) else None
                }
        print(projects)
        return Response(json.dumps(projects), mimetype="application/json")


    def _serve_static_file_from_directory(base_dir, path):
        path = os.path.join(base_dir, path)
        mime = magic.Magic(mime=True)
        mime_type = mime.from_file(path)
        with open(path, "r") as file_to_send:
            resp = Response(file_to_send.read(), mimetype=mime_type)

        return resp

    @app.route('/static/<path:path>')
    def static_serve(path):
        static_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
        return _serve_static_file_from_directory(static_directory, path)

    @app.route('/projects/<path:path>')
    def static_proxy(path):
        actual_path = os.path.join(work_dir, path)
        directory, filename = os.path.split(actual_path)
        if not actual_path.startswith(directory):
            abort(401)

        return _serve_static_file_from_directory(work_dir, path)

    publish_server = ThreadedServer(classpartial(PublishService, work_dir),
                                    port=12341)
    thread = threading.Thread(target=publish_server.start,
                              daemon=True)
    thread.start()

    app.run(port=port)


def main():
    arguments = docopt.docopt(__doc__)
    run_server(work_dir=os.path.abspath(arguments["--work-dir"]),
               port=int(arguments["--port"]),
               daemon=arguments["--daemon"])


if __name__ == "__main__":
    main()
