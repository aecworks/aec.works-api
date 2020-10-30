# Generated by Django 2.2.13 on 2020-10-30 03:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0027_thread_id_required'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='thread_size',
        ),
        migrations.RemoveField(
            model_name='post',
            name='thread_size',
        ),
        migrations.AddField(
            model_name='thread',
            name='size',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
