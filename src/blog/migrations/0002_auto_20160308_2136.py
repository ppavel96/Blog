# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-08 18:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='blog',
            field=models.CharField(max_length=100),
        ),
    ]