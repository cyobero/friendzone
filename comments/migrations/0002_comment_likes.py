# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-06 01:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='likes',
            field=models.IntegerField(null=True),
        ),
    ]