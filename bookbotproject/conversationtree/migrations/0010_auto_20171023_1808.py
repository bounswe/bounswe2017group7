# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-10-23 15:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conversationtree', '0009_auto_20171023_0148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='node',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
