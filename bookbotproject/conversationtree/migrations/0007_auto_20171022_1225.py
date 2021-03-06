# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-22 09:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('conversationtree', '0006_auto_20171019_2126'),
    ]

    operations = [
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(blank=True, max_length=100, unique=True)),
                ('intent', models.CharField(blank=True, max_length=100)),
                ('message', models.CharField(blank=True, max_length=500)),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='conversationtree.Node')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='conversationnode',
            name='parentNode',
        ),
        migrations.RemoveField(
            model_name='conversationtree',
            name='rootNode',
        ),
        migrations.DeleteModel(
            name='ConversationNode',
        ),
        migrations.DeleteModel(
            name='ConversationTree',
        ),
    ]
