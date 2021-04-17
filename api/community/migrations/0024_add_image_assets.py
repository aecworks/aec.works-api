# Generated by Django 2.2.13 on 2020-10-09 03:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0007_rename_image_asset'),
        ('community', '0023_post_images'),
    ]

    operations = [
        migrations.RenameField(
            model_name='company',
            old_name='twitter_handle',
            new_name='twitter',
        ),
        migrations.RenameField(
            model_name='companyrevision',
            old_name='twitter_handle',
            new_name='twitter',
        ),
        migrations.RenameField(
            model_name='post',
            old_name='cover_img',
            new_name='cover',
        ),
        migrations.AddField(
            model_name='company',
            name='cover',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='images.ImageAsset'),
        ),
        migrations.AddField(
            model_name='company',
            name='logo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='images.ImageAsset'),
        ),
        migrations.AddField(
            model_name='companyrevision',
            name='cover',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='images.ImageAsset'),
        ),
        migrations.AddField(
            model_name='companyrevision',
            name='logo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='images.ImageAsset'),
        ),
    ]
