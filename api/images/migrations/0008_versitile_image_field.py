# Generated by Django 2.2.13 on 2020-10-09 06:28

from django.db import migrations
import versatileimagefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0007_rename_image_asset'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imageasset',
            name='file',
            field=versatileimagefield.fields.VersatileImageField(height_field='height', upload_to='images/', width_field='width'),
        ),
    ]