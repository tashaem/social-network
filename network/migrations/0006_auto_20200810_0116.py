# Generated by Django 3.0.8 on 2020-08-09 18:16

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0005_auto_20200810_0109'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='likers',
        ),
        migrations.AddField(
            model_name='post',
            name='likers',
            field=models.ManyToManyField(blank=True, related_name='liked_posts', to=settings.AUTH_USER_MODEL),
        ),
    ]
