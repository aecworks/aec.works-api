import io
import datetime
import factory
from PIL import Image

from . import models


def png_bytes():
    image = Image.new("RGB", (1, 1))
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format="PNG")
    # b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00...'
    return img_byte_arr.getvalue()


class ImageAssetFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.ImageAsset

    file = factory.django.FileField(data=png_bytes(), filename="123.png")
    created_at = factory.LazyFunction(datetime.datetime.now)
    created_by = factory.SubFactory("api.users.factories.ProfileFactory")
