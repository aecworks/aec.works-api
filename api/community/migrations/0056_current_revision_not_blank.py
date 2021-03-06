# Generated by Django 2.2.20 on 2021-05-04 07:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0055_protect_images'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='current_revision',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='community.CompanyRevision'),
        ),
    ]
