# Generated by Django 3.0.8 on 2020-08-09 18:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0004_auto_20200806_2048'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='likes',
        ),
        migrations.AddField(
            model_name='post',
            name='likers',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='liked_posts', to=settings.AUTH_USER_MODEL),
        ),
    ]
