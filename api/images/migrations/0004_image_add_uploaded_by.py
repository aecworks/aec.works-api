# Generated by Django 2.2.12 on 2020-08-29 08:28

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('images', '0003_image_create_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='uploaded_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='images', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
