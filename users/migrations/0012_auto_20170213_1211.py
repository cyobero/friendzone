# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-13 18:11
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_auto_20170213_1128'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='follow',
            new_name='followers',
        ),
    ]
