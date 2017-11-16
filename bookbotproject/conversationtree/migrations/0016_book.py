# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-13 06:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conversationtree', '0015_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('isbn', models.CharField(max_length=1000)),
                ('title', models.CharField(blank=True, max_length=1000)),
                ('author', models.CharField(blank=True, max_length=1000)),
            ],
        ),
    ]
