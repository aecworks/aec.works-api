import requests
import io
import base64
import PIL

from django.core.files.images import ImageFile
from .utils import uuid_filename_from_content_type
from .models import ImageAsset


def create_image_asset(
    *, img_file, width=None, height=None, profile=None
) -> ImageAsset:
    if width or height:
        img_file = resize(img_file, width, height)
    return ImageAsset.objects.create(file=img_file, created_by=profile)


def create_image_file_from_data_uri(data_uri: str) -> ImageFile:
    """  Given a data-uri string, create a ImageFile object.
    eg. ("data:image/png;base64,iVBOR...") => ImageFile
    """
    #
    _, data = data_uri.split("data:")
    content_type, b64_data = data.split(";base64,")
    filename = uuid_filename_from_content_type(content_type)
    fp = io.BytesIO()
    fp.write(base64.b64decode(b64_data))
    return ImageFile(fp, name=filename)


def create_image_file_from_url(url, **kwargs) -> ImageFile:
    resp = requests.get(url, **kwargs)
    filename = uuid_filename_from_content_type(resp.headers["Content-Type"])
    fp = io.BytesIO()
    fp.write(resp.content)
    return ImageFile(fp, name=filename)


def resize(image_file, width, height):
    """
    Resizes Image using Pillow
    PIL's thumnail will set image size using the longest size and maintain
    aspect ratio.
    eg. If image is 500x100 and you provide 100x100 image will be 100x20
    """
    img = PIL.Image.open(image_file)

    img.thumbnail((width, height), PIL.Image.ANTIALIAS)
    new_file = io.BytesIO()
    img.save(new_file, img.format, quality=95)
    image_file.file = new_file
    image_file.size = new_file.getbuffer().nbytes
    return image_file
