# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-08 12:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('preview_post', models.TextField(max_length=200)),
                ('text', models.TextField()),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='ArticleImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article_image', models.FileField(blank=True, null=True, upload_to='media/articles/')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='zavod.Article')),
            ],
        ),
    ]