# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-22 10:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conversationtree', '0007_auto_20171022_1225'),
    ]

    operations = [
        migrations.AlterField(
            model_name='node',
            name='intent',
            field=models.CharField(blank=True, max_length=100, unique=True),
        ),
    ]
