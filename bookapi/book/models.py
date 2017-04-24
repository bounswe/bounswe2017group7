# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
LANGUAGE_CHOICES = sorted([('english','english'), ('turkish','turkish')])

class Book(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=50, blank=True, default='')
    author = models.CharField(max_length=50, blank=True, default='')
    language = models.CharField(choices=LANGUAGE_CHOICES, default='english', max_length=50)
    year = models.CharField(max_length=50, blank=True, default='')
    

    class Meta:
        ordering = ('created',)