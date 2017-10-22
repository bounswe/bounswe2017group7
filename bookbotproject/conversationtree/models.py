# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

class Node(MPTTModel):
    created = models.DateTimeField(auto_now_add=True)
    #Every node has a title name to describe their purpose.
    name = models.CharField(max_length=100, blank=True, unique=True)
    # Every node has an intent. (Will be used to choose which child the parent will select to go).
    intent = models.CharField(max_length=100, blank=True)
    # Every node has a parent. (Default parent is the root).
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)
    # Every node has a message that is going to be sent to the user when on that node.
    message = models.CharField(max_length=500, blank=True)

    def __unicode__(self):
        return self.name
    
    class MPTTMeta:
        order_insertion_by = ['name']
