# Generated by Django 2.2.20 on 2021-05-02 03:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0049_revision_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='companyrevision',
            name='approved_by',
        ),
    ]