# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-24 14:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='language',
            field=models.CharField(choices=[('english', 'english'), ('turkish', 'turkish')], default='english', max_length=50),
        ),
    ]
