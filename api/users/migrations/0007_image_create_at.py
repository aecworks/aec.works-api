# Generated by Django 2.2.12 on 2020-08-29 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_rename_source_provider'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='provider',
            field=models.CharField(choices=[('SIGN_UP', 'registration'), ('GITHUB', 'github'), ('LINKEDIN', 'linkedin')], default='registration', max_length=16),
        ),
    ]
