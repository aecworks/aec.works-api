# Generated by Django 2.2.12 on 2020-08-25 06:07

from django.db import migrations, models

import api.common.mixins


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0012_temp_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images')),
            ],
            bases=(api.common.mixins.ReprMixin, models.Model),
        ),
        migrations.RemoveField(
            model_name='company',
            name='cover',
        ),
        migrations.RemoveField(
            model_name='company',
            name='logo',
        ),
        migrations.RemoveField(
            model_name='companyrevision',
            name='cover',
        ),
        migrations.RemoveField(
            model_name='companyrevision',
            name='logo',
        ),
        migrations.AddField(
            model_name='company',
            name='cover_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='company',
            name='logo_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='companyrevision',
            name='cover_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='companyrevision',
            name='logo_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
