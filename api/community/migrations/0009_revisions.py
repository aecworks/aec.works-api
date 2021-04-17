# Generated by Django 2.2.12 on 2020-08-12 05:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_profile_slug'),
        ('community', '0008_created_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='last_revision',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='community.CompanyRevision'),
        ),
        migrations.AddField(
            model_name='companyrevision',
            name='approved_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='company_approvals', to='users.Profile'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='companyrevision',
            name='applied',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='companyrevision',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='company_revisions', to='users.Profile'),
        ),
    ]
