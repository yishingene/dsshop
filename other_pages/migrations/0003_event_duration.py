# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-05-26 09:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('other_pages', '0002_auto_20170526_0856'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='duration',
            field=models.PositiveIntegerField(default=1, verbose_name='aantal dagen'),
        ),
    ]