# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-23 10:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('conversationtree', '0008_auto_20171022_1313'),
    ]

    operations = [
        migrations.CreateModel(
            name='TelegramUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(blank=True, max_length=100)),
                ('userid', models.IntegerField(unique=True)),
                ('chatid', models.IntegerField(unique=True)),
                ('currentnode', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='conversationtree.Node')),
            ],
        ),
    ]