# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-05-13 07:09
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0014_auto_20170502_1828'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='description_en',
        ),
        migrations.RemoveField(
            model_name='category',
            name='name_en',
        ),
        migrations.RemoveField(
            model_name='product',
            name='description_en',
        ),
        migrations.RemoveField(
            model_name='product',
            name='title_en',
        ),
    ]
