# Generated by Django 2.2.12 on 2020-05-12 03:19

import api.common.mixins
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0007_auto_20200511_0633'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommentThread',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            bases=(api.common.mixins.ReprMixin, models.Model),
        ),
        migrations.RemoveField(
            model_name='company',
            name='root_comment',
        ),
        migrations.RemoveField(
            model_name='post',
            name='root_comment',
        ),
        migrations.AddField(
            model_name='comment',
            name='thread',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='community.CommentThread'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='company',
            name='comment_thread',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='community.CommentThread'),
        ),
        migrations.AddField(
            model_name='post',
            name='comment_thread',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='community.CommentThread'),
        ),
    ]
