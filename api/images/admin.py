from django.contrib import admin

from . import models


@admin.register(models.Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ["image", "created_at", "created_by"]
