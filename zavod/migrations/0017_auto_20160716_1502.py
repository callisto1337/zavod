# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-16 15:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zavod', '0016_article_published'),
    ]

    operations = [
        migrations.AddField(
            model_name='categoryproduct',
            name='published',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='product',
            name='published',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='subcategoryproduct',
            name='published',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='title',
            field=models.CharField(max_length=100),
        ),
    ]
