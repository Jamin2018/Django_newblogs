# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-19 09:51
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='article_typy',
            new_name='article_type',
        ),
    ]
