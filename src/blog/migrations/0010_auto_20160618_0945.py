# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-06-18 06:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_auto_20160617_2243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='voteforcomment',
            name='like',
            field=models.SmallIntegerField(default=0),
        ),
    ]
