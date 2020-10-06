from django.utils.html import format_html
from django.contrib import admin

from . import models


@admin.register(models.ImageAsset)
class ImageAdmin(admin.ModelAdmin):
    list_display = ["id", "file", "created_at", "created_by", "thumbnail"]

    def thumbnail(self, obj):
        return format_html(f'<img height="32" src="{obj.file.url}"/>')

    thumbnail.short_description = "Thumbnail"
