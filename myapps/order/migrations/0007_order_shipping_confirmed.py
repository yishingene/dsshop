# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-09-23 08:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0006_order_language'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='shipping_confirmed',
            field=models.BooleanField(default=False),
        ),
    ]
