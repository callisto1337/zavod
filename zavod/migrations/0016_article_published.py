# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-16 14:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zavod', '0015_auto_20160715_1254'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='published',
            field=models.BooleanField(default=True),
        ),
    ]