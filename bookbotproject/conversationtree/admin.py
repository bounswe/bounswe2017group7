# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Node, TelegramUser, Template, Comment, Book

admin.site.register(Node,
                    MPTTModelAdmin,
                    list_display=('name', 'intent', 'message',),
                    list_display_links=('name',)
                    ,)
admin.site.register(TelegramUser, list_display=('__unicode__', 'currentnode',),
                                       list_display_links=('__unicode__',),)
admin.site.register(Template,
                    admin.ModelAdmin,
                    list_filter=('node', ),
                    list_display=('template', 'node',),
                    list_display_links=('template',)
                    ,)
admin.site.register(Book,
                    admin.ModelAdmin,
                    list_filter=('author', 'genre'),
                    list_display=('__unicode__', 'author', 'genre'),
                    list_display_links=('__unicode__',)
                    ,)
admin.site.register(Comment,
                    admin.ModelAdmin,
                    list_filter=('user', 'book'),
                    list_display=('__unicode__', 'user', 'comment', 'book'),
                    list_display_links=('__unicode__',),)
