from django.utils.html import format_html
from django.contrib import admin

from . import models


@admin.register(models.ImageAsset)
class ImageAdmin(admin.ModelAdmin):
    list_display = ["file", "created_at", "created_by"]
