# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-19 10:31
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0002_auto_20171219_1751'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='article_type',
        ),
        migrations.DeleteModel(
            name='ArticleType',
        ),
    ]
