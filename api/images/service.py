import requests
import io

from django.core.files.images import ImageFile

from .models import Image


def create_image(*, image_file, user=None) -> Image:
    return Image.objects.create(image=image_file, created_by=user)


def create_image_from_url(url, **kwargs):
    resp = requests.get(url, **kwargs)
    extension = resp.headers["Content-Type"].split("image/")[1]
    fp = io.BytesIO()
    fp.write(resp.content)
    image = ImageFile(fp, name=f"_.{extension}")
    return create_image(image_file=image)
