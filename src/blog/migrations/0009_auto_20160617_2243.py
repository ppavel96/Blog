# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-06-17 19:43
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_auto_20160617_2117'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='cachedSubscriptionsNumber',
            new_name='cachedPostFollowersNumber',
        ),
    ]
