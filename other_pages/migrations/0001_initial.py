# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-05-25 06:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='naam')),
                ('date', models.DateField(verbose_name='datum')),
                ('website', models.URLField(verbose_name='website link')),
                ('location', models.CharField(max_length=64, verbose_name='locatie (stad)')),
            ],
            options={
                'verbose_name_plural': 'beurzen',
                'ordering': ['-date'],
                'verbose_name': 'beurs',
            },
        ),
    ]
