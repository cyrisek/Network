# Generated by Django 4.1.3 on 2022-11-06 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_profile_post'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='likes',
        ),
        migrations.AddField(
            model_name='post',
            name='likes',
            field=models.BooleanField(default=False),
        ),
    ]
