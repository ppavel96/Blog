# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-08 20:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_auto_20160308_2339'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='img',
            field=models.CharField(default='null', max_length=200),
        ),
    ]