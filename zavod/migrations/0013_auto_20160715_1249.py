# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-15 12:49
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('zavod', '0012_auto_20160715_1239'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='product_category',
            new_name='category',
        ),
    ]