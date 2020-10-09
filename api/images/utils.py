from uuid import uuid4
from rest_framework.parsers import FileUploadParser
from rest_framework.exceptions import ParseError


class UuidNamedFileUploadParser(FileUploadParser):
    def get_filename(self, stream, media_type, parser_context):
        request = parser_context["request"]
        return uuid_filename_from_content_type(request.content_type)


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
