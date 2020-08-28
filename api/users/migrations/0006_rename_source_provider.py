# Generated by Django 2.2.12 on 2020-08-28 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_avatar_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='source',
        ),
        migrations.AddField(
            model_name='user',
            name='provider',
            field=models.CharField(choices=[('SIGN_UP', 'registration'), ('GITHUB', 'github'), ('LINKEDIN', 'linkedIn')], default='registration', max_length=16),
        ),
    ]
