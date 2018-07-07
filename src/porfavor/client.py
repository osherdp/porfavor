"""Publish documentation for a project on the server.

Usage:
    client.py <host> <project> <directory>
    client.py -h | --help

Options:
    -h --help           Display help message and exit.
"""
import os

import rpyc
import tqdm
import docopt


def walk_directory(root):
    for file_root, _, files in os.walk(root):
        for file_name in files:
            yield os.path.join(file_root, file_name)


def get_files_contents(root):
    files_count = sum(1 for _ in walk_directory(root))
    for path in tqdm.tqdm(walk_directory(root),
                          total=files_count,
                          unit=" files"):
        with open(path, "rb") as f:
            yield os.path.relpath(path, root), f.read()


def publish(host, project, root_dir):
    print("Connecting to host on {}...".format(host))
    client = rpyc.connect(host, 12341)
    print("Connected successfully!")

    print("Publishing content for project '{}'".format(project))
    client.root.publish(project, get_files_contents(root_dir))
    print("Finished publishing successfully!")


def main():
    arguments = docopt.docopt(__doc__)
    publish(host=arguments["<host>"],
            project=arguments["<project>"],
            root_dir=arguments["<directory>"])


if __name__ == "__main__":
    main()
