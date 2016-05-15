# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-05-15 16:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_tag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='cachedBlogRating',
            field=models.PositiveIntegerField(default=0, editable=False),
        ),
        migrations.AlterField(
            model_name='blog',
            name='cachedMembersNumber',
            field=models.PositiveIntegerField(default=0, editable=False),
        ),
        migrations.AlterField(
            model_name='blog',
            name='cachedPostsNumber',
            field=models.PositiveIntegerField(default=0, editable=False),
        ),
        migrations.AlterField(
            model_name='post',
            name='cachedCommentsNumber',
            field=models.PositiveIntegerField(default=0, editable=False),
        ),
        migrations.AlterField(
            model_name='post',
            name='cachedRating',
            field=models.PositiveIntegerField(default=0, editable=False),
        ),
        migrations.AlterField(
            model_name='post',
            name='cachedSubscriptionsNumber',
            field=models.PositiveIntegerField(default=0, editable=False),
        ),
        migrations.AlterField(
            model_name='profile',
            name='cachedCommentsNumber',
            field=models.PositiveIntegerField(default=0, editable=False),
        ),
        migrations.AlterField(
            model_name='profile',
            name='cachedFollowersNumber',
            field=models.PositiveIntegerField(default=0, editable=False),
        ),
        migrations.AlterField(
            model_name='profile',
            name='cachedPostsNumber',
            field=models.PositiveIntegerField(default=0, editable=False),
        ),
        migrations.AlterField(
            model_name='profile',
            name='cachedSubscriptionsForBlogNumber',
            field=models.PositiveIntegerField(default=0, editable=False),
        ),
        migrations.AlterField(
            model_name='profile',
            name='cachedSubscriptionsForPostNumber',
            field=models.PositiveIntegerField(default=0, editable=False),
        ),
        migrations.AlterField(
            model_name='profile',
            name='cachedSubscriptionsForUserNumber',
            field=models.PositiveIntegerField(default=0, editable=False),
        ),
        migrations.AlterField(
            model_name='profile',
            name='cachedUserRating',
            field=models.PositiveIntegerField(default=0, editable=False),
        ),
        migrations.AlterField(
            model_name='tag',
            name='cachedTagNumber',
            field=models.PositiveIntegerField(default=0, editable=False),
        ),
    ]
