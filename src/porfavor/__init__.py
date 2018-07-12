"""Manage documentation in a client-server architecture.

Usage:
    porfavor serve [--work-dir <dir>] [--host <host>] [-p <port> | --port <port>]
                   [-D | --daemon]
    porfavor publish <host> <project> <directory>
    porfavor -h | --help

Options:
    --work-dir <dir>            Directory to server files under it [Default: .].
    --host <host>               Host ip address of the server [Default: 0.0.0.0].
    --port <port> -p <port>     Port for the web server [Default: 5000].
    -D --daemon                 Run in the background.
"""
import docopt

from .client import publish
from .server import run_server


def main():
    arguments = docopt.docopt(__doc__)
    if arguments["serve"]:
        run_server(host=arguments["--host"],
                   work_dir=arguments["--work-dir"],
                   port=arguments["--port"],
                   daemon=arguments["--daemon"])

    if arguments["publish"]:
        publish(host=arguments["<host>"],
                project=arguments["<project>"],
                root_dir=arguments["<directory>"])


if __name__ == "__main__":
    main()
