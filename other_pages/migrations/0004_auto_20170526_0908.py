# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-05-26 09:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('other_pages', '0003_event_duration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='date',
            field=models.DateField(verbose_name='startdatum'),
        ),
    ]
