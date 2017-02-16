# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-11 23:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0006_auto_20170211_1737'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='likes',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='parent',
        ),
        migrations.AddField(
            model_name='comment',
            name='reply',
            field=models.TextField(blank=True, null=True),
        ),
    ]