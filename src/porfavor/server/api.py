"""All public API for javascript client and other clients."""
# pylint: disable=no-member
from __future__ import absolute_import

import os
import json
import zipfile
import http.client

from flask import Blueprint, request, current_app, Response

api = Blueprint("api", __name__)  # pylint: disable=invalid-name


@api.route('/get_projects')
def get_projects():
    """Map every project to its info."""
    work_dir = current_app.config["UPLOAD_FOLDER"]
    projects = {}
    for path in os.listdir(work_dir):
        if not os.path.isdir(os.path.join(work_dir, path)):
            continue

        icon_path = os.path.join(work_dir, path, "icon.png")
        revealed_icon_path = os.path.join("projects", path, "icon.png")
        projects[path] = {
            "icon": revealed_icon_path if os.path.exists(icon_path) else None
        }

    return Response(json.dumps(projects), mimetype="application/json")


@api.route('/upload_docs', methods=["PUT"])
def upload_documentation():
    """Enable deployment of documentation files."""
    if not request.files:
        return ("No file was supplied in the request",
                http.client.BAD_REQUEST)

    for doc_file in request.files.values():
        if doc_file.filename == "":
            return ("Documentation file name is empty",
                    http.client.BAD_REQUEST)

        if not doc_file.filename.endswith(".zip"):
            return ("Documentation file {} is not a zip file".format(doc_file),
                    http.client.BAD_REQUEST)

        local_zip_path = os.path.join(current_app.config["UPLOAD_FOLDER"],
                                      doc_file.filename)
        doc_file.save(local_zip_path)

        with zipfile.ZipFile(local_zip_path) as zip_file:
            destination_dir, _ = os.path.splitext(local_zip_path)
            zip_file.extractall(destination_dir)

    return "", http.client.NO_CONTENT
