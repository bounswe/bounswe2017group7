# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class ConversationNode(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    #Every node has a title to describe their purpose.
    title = models.CharField(max_length=100, blank=True)
    # Every node has an intent. (Will be used to choose which child the parent will select to go).
    intent = models.CharField(max_length=50, blank=True)
    # Every node has a parent. (Default parent is the root).
    parentNode = models.ForeignKey('self', default=1)
    # Every node has a message that is going to be sent to the user when on that node.
    message = models.CharField(max_length=500, blank=True)
    
    class Meta:
        ordering = ('created',)

class ConversationTree(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=50)
    rootNode = models.ForeignKey(ConversationNode, default=1)

    class Meta:
        ordering = ('created',)
