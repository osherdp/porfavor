"""Run the hosting documentation server.

Usage:
    porfavor-server [--work-dir <dir>] [-D|--daemon]
    porfavor-server -h | --help

Options:
    -h --help           Display help message and exit.
    --work-dir <dir>    Directory to server files under it [default: .]
    -D --daemon         Run in the background.
"""
from __future__ import print_function
import os
import threading

import rpyc
import docopt
from flask import Flask, send_from_directory, render_template, abort


class PublishService(rpyc.Service):
    def exposed_publish(self, project, project_docs):
        for relative_path, content in project_docs:
            path = os.path.join(os.path.abspath("."),
                                project,
                                relative_path)
            directory = os.path.dirname(path)

            if not os.path.isdir(directory):
                os.makedirs(directory)

            with open(path, "wb") as f:
                f.write(content)


def run_server(work_dir, daemon):
    os.chdir(work_dir)

    app = Flask(__name__)

    @app.route('/')
    def root():
        projects = [filename for filename in os.listdir(work_dir)
                    if os.path.isdir(os.path.join(work_dir, filename))]

        return render_template("index.html",
                               projects=projects)

    @app.route('/<path:path>')
    def static_proxy(path):
        path = os.path.abspath(path)
        directory, filename = os.path.split(path)
        if not path.startswith(directory):
            abort(401)

        return send_from_directory(directory, filename)

    publish_server = rpyc.utils.server.ThreadedServer(PublishService,
                                                      port=12341)
    thread = threading.Thread(target=publish_server.start,
                              daemon=True)
    thread.start()

    app.run()


def main():
    arguments = docopt.docopt(__doc__)
    run_server(work_dir=arguments["--work-dir"],
               daemon=arguments["--daemon"])


if __name__ == "__main__":
    main()
