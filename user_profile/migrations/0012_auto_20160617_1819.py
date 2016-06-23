# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-17 22:19
from __future__ import unicode_literals

from django.db import migrations, models
import user_profile.models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0011_auto_20160617_1803'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='picture',
            field=models.ImageField(default='quicktutorsApp/media/user-character.png', upload_to=user_profile.models.user_directory_path),
        ),
    ]