# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-11 18:12
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('zavod', '0006_auto_20160711_1809'),
    ]

    operations = [
        migrations.RenameField(
            model_name='categoryproduct',
            old_name='category_name',
            new_name='name',
        ),
    ]