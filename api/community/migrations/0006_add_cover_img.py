# Generated by Django 2.2.12 on 2020-08-10 02:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0005_rename_editor_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='cover',
            field=models.ImageField(blank=True, null=True, upload_to='covers'),
        ),
        migrations.AlterField(
            model_name='company',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to='logos'),
        ),
    ]
