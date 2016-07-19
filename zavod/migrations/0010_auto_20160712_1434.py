# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-12 14:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zavod', '0009_auto_20160712_1052'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subproduct',
            name='product_category',
        ),
        migrations.AlterField(
            model_name='categoryproduct',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='categoryproduct',
            name='slug',
            field=models.SlugField(default='', max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(default='', max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='subproduct',
            name='slug',
            field=models.SlugField(default='', max_length=100, unique=True),
        ),
    ]