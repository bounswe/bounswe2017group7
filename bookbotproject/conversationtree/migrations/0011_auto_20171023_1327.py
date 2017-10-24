# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-23 10:27
from __future__ import unicode_literals

from django.db import migrations
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('conversationtree', '0010_merge_20171023_1325'),
    ]

    operations = [
        migrations.AlterField(
            model_name='telegramuser',
            name='currentnode',
            field=mptt.fields.TreeForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='conversationtree.Node'),
        ),
    ]