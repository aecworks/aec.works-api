from pathlib import Path
from uuid import uuid4
from functools import partial
from rest_framework.parsers import FileUploadParser
from rest_framework.exceptions import ParseError


class UuidNamedFileUploadParser(FileUploadParser):
    """
    TODO
    """

    def get_filename(self, stream, media_type, parser_context):
        request = parser_context["request"]
        return uuid_filename_from_content_type(request.content_type)


def _generate_filename(path, instance, filename):
    random_filename = f"{uuid4().hex}{Path(filename).suffix}"
    return Path(path) / random_filename


def uuid_filename_from_content_type(content_type: str) -> str:
    supported_types = {
        "image/jpeg": "jpg",
        "image/png": "png",
    }
    try:
        extension = supported_types[content_type]
    except KeyError:
        raise ParseError(f"content-type not supported: {content_type}")
    return f"{uuid4().hex}.{extension}"


generate_image_path_partial = partial(_generate_filename, "images")
