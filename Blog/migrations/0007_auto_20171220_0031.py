# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-19 16:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0006_auto_20171219_2203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='title',
            field=models.CharField(max_length=32, unique=True, verbose_name='分类标题'),
        ),
    ]