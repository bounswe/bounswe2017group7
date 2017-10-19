# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-19 15:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('conversationtree', '0002_conversationnode'),
    ]

    operations = [
        migrations.AddField(
            model_name='conversationtree',
            name='rootNode',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='conversationtree.ConversationNode'),
        ),
    ]
