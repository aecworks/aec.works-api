# Generated by Django 2.2.20 on 2021-04-16 02:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0030_opengraph_blank'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['created_at']},
        ),
        migrations.RemoveField(
            model_name='comment',
            name='level',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='lft',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='parent',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='reply_count',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='rght',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='tree_id',
        ),
        migrations.RemoveField(
            model_name='thread',
            name='size',
        ),
    ]