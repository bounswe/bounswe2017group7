# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.utils import timezone

class Node(MPTTModel):
    created = models.DateTimeField(default=timezone.now)
    #Every node has a title name to describe their purpose.
    name = models.CharField(max_length=100, blank=True, unique=True)
    # Every node has an intent. (Will be used to choose which child the parent will select to go).
    intent = models.CharField(max_length=100, blank=True, unique=True)
    # Every node has a parent. (Default parent is the root).
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)
    # Every node has a message that is going to be sent to the user when on that node.
    message = models.CharField(max_length=500, blank=True)

    def __unicode__(self):
        return self.name
    
    class MPTTMeta:
        order_insertion_by = ['name']

class TelegramUser(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    # Telegram user can have a name if they choose to provide one.
    name = models.CharField(max_length=100, blank=True)
    # Telegram user has an id.
    userid = models.IntegerField(unique=True)
    # Telegram user has a chat id
    chatid = models.IntegerField(unique=True)
    # Telegram user has their current node in the conversation tree.
    currentnode = TreeForeignKey(Node, blank=True)

    def __unicode__(self):
        return (str(self.userid) + " - " + self.name)
    
    class MPTTMeta:
        order_insertion_by = ['name']

        
class Template(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    # This template belongs to a node.
    node = TreeForeignKey(Node)
    is_trained = models.BooleanField(default=False)
    template = models.CharField(max_length=500)
 
    class MPTTMeta:
        order_insertion_by = ['node']

        
class Book(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    # Every book has unique isbn
    isbn = models.CharField(max_length=100, blank = True)
    # We may know the title of the book.
    title = models.CharField(max_length=100)
    # We may know the author of the book.
    author = models.CharField(max_length=100, blank = True)
    # We may know the genre of the book.
    genre = models.CharField(max_length=100, blank = True)
    
    def __unicode__(self):
        return (str(self.isbn) + " - " + self.title)

    class MPTTMeta:
        order_insertion_by = ['title']

class Comment(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    # This comment belongs to a user.
    user = models.ForeignKey(TelegramUser)
    # This comment has a text.
    comment = models.CharField(max_length=1000)
    # This comment may or may not be flagged by admins/mods.By default, it is not flagged.
    isFlagged = models.BooleanField(default=False)
    # This comment is going to belong to a book.
    book = models.ForeignKey(Book, null = True)

    def __unicode__(self):
        return (("flagged comment #" if self.isFlagged else "default comment #") + str(self.id))

    class MPTTMeta:
        order_insertion_by = ['created']

RATE_CHOICES = [(1,1), (2,2), (3,3), (4,4), (5,5)]
class Rate(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    # This rate belongs to a user.
    user = models.ForeignKey(TelegramUser)
    # This rate has a value.
    value = models.IntegerField(choices=RATE_CHOICES)
    # This rate is going to belong to a book.
    book = models.ForeignKey(Book, null = True)

    def __unicode__(self):
        return ("Rate of " + self.book.title + " by user " + self.user.name)

    class MPTTMeta:
        order_insertion_by = ['created']
