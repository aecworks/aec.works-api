# Generated by Django 2.2.12 on 2020-08-12 05:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0010_rev_hashtags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companyrevision',
            name='approved_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='company_approvals', to='users.Profile'),
        ),
    ]
