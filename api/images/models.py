from django.db import models
from versatileimagefield.fields import VersatileImageField

from api.common.mixins import ReprMixin


class ImageAsset(ReprMixin, models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        "users.Profile",
        related_name="images_files",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    file = VersatileImageField(
        upload_to="images/",
        width_field="width",
        height_field="height",
    )

    height = models.PositiveIntegerField(blank=True, null=True)
    width = models.PositiveIntegerField(blank=True, null=True)
