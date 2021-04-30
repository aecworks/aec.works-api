# Generated by Django 2.2.20 on 2021-04-29 21:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0037_current_revision_rename'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='banner',
        ),
        migrations.RemoveField(
            model_name='company',
            name='cover',
        ),
        migrations.RemoveField(
            model_name='company',
            name='crunchbase_id',
        ),
        migrations.RemoveField(
            model_name='company',
            name='description',
        ),
        migrations.RemoveField(
            model_name='company',
            name='hashtags',
        ),
        migrations.RemoveField(
            model_name='company',
            name='location',
        ),
        migrations.RemoveField(
            model_name='company',
            name='logo',
        ),
        migrations.RemoveField(
            model_name='company',
            name='name',
        ),
        migrations.RemoveField(
            model_name='company',
            name='twitter',
        ),
        migrations.RemoveField(
            model_name='company',
            name='website',
        ),
        migrations.RemoveField(
            model_name='post',
            name='companies',
        ),
        migrations.AddField(
            model_name='companyrevision',
            name='banner',
            field=models.CharField(blank=True, default='', max_length=32),
        ),
    ]
