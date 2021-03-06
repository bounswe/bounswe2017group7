# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-24 13:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(blank=True, default='', max_length=50)),
                ('author', models.CharField(blank=True, default='', max_length=50)),
                ('language', models.CharField(choices=[('en', 'English'), ('tr', 'Turkish')], default='English', max_length=50)),
                ('year', models.CharField(blank=True, default='', max_length=50)),
            ],
            options={
                'ordering': ('created',),
            },
        ),
    ]
