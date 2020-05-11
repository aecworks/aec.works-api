# Generated by Django 2.2.12 on 2020-05-11 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0004_auto_20200511_0618'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='slug',
            field=models.CharField(blank=True, max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.CharField(blank=True, max_length=100, unique=True),
        ),
    ]
