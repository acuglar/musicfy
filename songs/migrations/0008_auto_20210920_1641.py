# Generated by Django 3.2.5 on 2021-09-20 16:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('songs', '0007_auto_20210917_1852'),
    ]

    operations = [
        migrations.AddField(
            model_name='playlist',
            name='collaborators',
            field=models.ManyToManyField(related_name='playlists', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='playlist',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='my_playlists', to='auth.user'),
            preserve_default=False,
        ),
    ]
