# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-15 12:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('zavod', '0013_auto_20160715_1249'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='subcategory',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='zavod.SubCategoryProduct'),
        ),
    ]