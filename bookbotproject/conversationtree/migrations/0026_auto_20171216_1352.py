# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-16 10:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conversationtree', '0025_auto_20171216_1320'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rate',
            name='book',
        ),
        migrations.RemoveField(
            model_name='rate',
            name='user',
        ),
        migrations.AddField(
            model_name='rate',
            name='book_title',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='rate',
            name='user_id',
            field=models.IntegerField(null=True),
        ),
    ]
