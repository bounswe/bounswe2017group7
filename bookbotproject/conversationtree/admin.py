# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Node, Template
    
admin.site.register(Node,
                    MPTTModelAdmin,
                    list_display=('name', 'intent', 'message',),
                    list_display_links=('name',)
                    ,)
admin.site.register(Template,
                    admin.ModelAdmin,
                    list_filter=('node', ),
                    list_display=('template', 'node',),
                    list_display_links=('template',)
                    ,)
