# Generated by Django 2.2.12 on 2020-08-25 06:49
import functools
from functools import partial
from pathlib import Path
from uuid import uuid4

from django.db import migrations, models


def _generate_filename(path, instance, filename):
    random_filename = f"{uuid4().hex}{Path(filename).suffix}"
    return Path(path) / random_filename


generate_image_path_partial = partial(_generate_filename, "images")


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Image",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        upload_to=functools.partial(
                            generate_image_path_partial, *("images",), **{}
                        )
                    ),
                ),
            ],
        ),
    ]
