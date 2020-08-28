from django.db import models

from api.common.mixins import ReprMixin
from .utils import generate_image_path_partial


class Image(ReprMixin, models.Model):
    image = models.ImageField(upload_to=generate_image_path_partial)
