from pathlib import Path
from uuid import uuid4
from django.db import models
from functools import partial

from api.common.mixins import ReprMixin


def generate_filename(path, instance, filename):
    random_filename = f"{uuid4().hex}{Path(filename).suffix}"
    return Path(path) / random_filename


generate_image_path = partial(generate_filename, "images")


class Image(ReprMixin, models.Model):
    image = models.ImageField(upload_to=generate_image_path)
