# Generated by Django 2.2.20 on 2021-04-29 21:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0036_company_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='company',
            old_name='last_revision',
            new_name='current_revision',
        ),
    ]