# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-08 20:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20160308_2332'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='img',
            field=models.CharField(default='no', max_length=200),
        ),
    ]
