# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-18 19:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='updown',
            name='article',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='Blog.Article', verbose_name='点赞的文章'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='updown',
            name='up',
            field=models.BooleanField(default=1, verbose_name='是否赞过'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='updown',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Blog.UserInfo', verbose_name='赞或踩的用户'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='updown',
            unique_together=set([('article', 'user')]),
        ),
    ]
