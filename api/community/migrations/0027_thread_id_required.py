# Generated by Django 2.2.13 on 2020-10-29 02:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0026_add_counts'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='thread',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='community.Thread'),
        ),
    ]
