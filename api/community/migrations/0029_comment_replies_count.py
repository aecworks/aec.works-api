# Generated by Django 2.2.13 on 2020-10-30 03:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("community", "0028_thread_size_in_thread"),
    ]

    operations = [
        migrations.AddField(
            model_name="comment",
            name="reply_count",
            field=models.PositiveIntegerField(default=0),
        ),
    ]
