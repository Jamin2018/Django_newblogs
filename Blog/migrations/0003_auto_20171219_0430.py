# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-18 20:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0002_auto_20171219_0346'),
    ]

    operations = [
        migrations.AlterField(
            model_name='updown',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='updown', to='Blog.UserInfo', verbose_name='赞或踩的用户'),
        ),
    ]
