from django.db import models
from django.contrib.auth import get_user_model
from api.common.mixins import ReprMixin
from .utils import generate_image_path_partial

User = get_user_model()


class Image(ReprMixin, models.Model):
    image = models.ImageField(upload_to=generate_image_path_partial)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User, related_name="images", on_delete=models.PROTECT, null=True, blank=True
    )
