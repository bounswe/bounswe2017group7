# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import ConversationTree, ConversationNode

# Register your models here.
admin.site.register(ConversationTree)
admin.site.register(ConversationNode)
