# Generated by Django 2.2.13 on 2020-10-09 04:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0024_add_image_assets'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='cover_url',
        ),
        migrations.RemoveField(
            model_name='company',
            name='logo_url',
        ),
        migrations.RemoveField(
            model_name='companyrevision',
            name='cover_url',
        ),
        migrations.RemoveField(
            model_name='companyrevision',
            name='logo_url',
        ),
    ]