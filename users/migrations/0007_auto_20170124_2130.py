# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-24 21:30
from __future__ import unicode_literals

from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20170124_1939'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_pic',
            field=models.ImageField(default='default.jpg', upload_to=users.models.upload_location),
        ),
    ]