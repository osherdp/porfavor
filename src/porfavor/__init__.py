"""Manage documentation in a client-server architechture.

Usage:
    porfavor serve [--work-dir <dir>] [-D|--daemon]
    porfavor publish <host> <project> <directory>
    porfavor -h | --help

Options:
    --work-dir <dir>    Directory to server files under it [default: .]
    -D --daemon         Run in the background.
"""
import docopt

from .client import publish
from .server import run_server


def main():
    arguments = docopt.docopt(__doc__)
    if arguments["serve"]:
        run_server(work_dir=arguments["--work-dir"],
                   daemon=arguments["--daemon"])

    if arguments["publish"]:
        publish(host=arguments["<host>"],
                project=arguments["<project>"],
                root_dir=arguments["<directory>"])


if __name__ == "__main__":
    main()
