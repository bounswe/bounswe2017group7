# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-19 19:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conversationtree', '0026_auto_20171216_1352'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='title',
            field=models.CharField(max_length=100),
        ),
    ]