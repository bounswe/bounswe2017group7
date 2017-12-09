# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from conversationtree.models import Node
from conversationtree.models import Comment
from conversationtree.models import Rate
from conversationtree.models import Book
from serializers import NodeSerializer
from conversationtree.models import TelegramUser
from serializers import TelegramUserSerializer
from witapi import *

# Create your views here.
@csrf_exempt
def node_list(request):
    """
    List all nodes, or create a new node.
    """
    if request.method == 'GET':
        nodes = Node.objects.all()
        serializer = NodeSerializer(nodes, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = NodeSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def nodes_detail(request, pk):
    """
    Retrieve, update or delete a node.
    """
    try:
        node = Node.objects.get(intent=pk)
    except Node.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = NodeSerializer(node)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = NodeSerializer(node, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        node.delete()
        return HttpResponse(status=204)

@csrf_exempt
def get_user_info(request, pk):
    """
    Gets user info if it exists, otherwise creates new one 
    """
    try:
        user = TelegramUser.objects.get(userid=pk)
    except TelegramUser.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = TelegramUserSerializer(user)
        return JsonResponse(serializer.data)


@csrf_exempt
def add_new_user(request, _name, _userid, _chatid):
    """
    Gets user info if it exists, otherwise creates new one 
    """
    try:
        node = Node.objects.get(intent="root")
    except Node.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'POST':
        newUser = TelegramUser.objects.create(name=_name, userid=_userid, chatid = _chatid, currentnode = node)
        return HttpResponse(status=200)



@csrf_exempt
def add_comment (  request, _title, _userid, _comment ):
    _title_conv = _title.replace('_', ' ')
    _comment_conv =_comment.replace('_', ' ')
    if request.method == 'POST':
        try:
            commentbook = Book.objects.get(title=_title_conv)
        except:
            Book.objects.create(title=_title_conv)
            commentbook = Book.objects.get(title=_title_conv)
        _user = TelegramUser.objects.get(userid=_userid)
        newComment = Comment.objects.create( user=_user,comment=_comment_conv, book = commentbook)
        return HttpResponse(status=200)

@csrf_exempt
def add_rating (  request, _title, _userid, _rating ):
    _title_conv = _title.replace('_', ' ')
    try:
        ratebook = Book.objects.get(title=_title_conv)
    except:
        Book.objects.create(title=_title_conv)
        ratebook = Book.objects.get(title=_title_conv)
    _user = TelegramUser.objects.get(userid=_userid)
    newRating = Rate.objects.create( user=_user,value=int(_rating), book = ratebook)
    return HttpResponse(status=200)


def get_response(request, _message, _chatid):
    """ waits until a response from wit ai, it may take so much time !!!!"""

    if request.method == 'GET':
        intent_ret = None
        intent_count = 0
        while intent_ret == None and intent_count<6:
            intent_count = intent_count + 1
            intent_ret = get_Intent(_message)


        curr_user = TelegramUser.objects.get(chatid=_chatid)
        curr_node = curr_user.currentnode

        print(curr_node.intent)
        if intent_ret is None and str(curr_node.intent) != 'comment_on_book' and str(curr_node.intent) != 'book_name_comment' and str(curr_node.intent) != 'rate_book' and str(curr_node.intent) != 'book_name_rating':
            return JsonResponse('I couldn\'t understand can you express it more simple?', safe=False)
        elif intent_ret == 'end_dialog':
            curr_user.currentnode=Node.objects.all()[0]
            curr_user.save()
            return JsonResponse('Goodbye bookworm!', safe=False)
        elif curr_node.intent == 'comment_on_book':
            curr_user.currentnode=curr_node.get_children()[0]
            curr_user.save()
            return JsonResponse(curr_user.currentnode.message, safe=False)
        elif curr_node.intent == 'book_name_comment':
            curr_user.currentnode=Node.objects.all()[0]
            curr_user.save()
            return JsonResponse('Your comment is saved!', safe=False)
        elif curr_node.intent == 'rate_book':
            curr_user.currentnode=curr_node.get_children()[0]
            curr_user.save()
            return JsonResponse(curr_user.currentnode.message, safe=False)
        elif curr_node.intent == 'book_name_rating':
            curr_user.currentnode=Node.objects.all()[0]
            curr_user.save()
            return JsonResponse('Your rating is saved!', safe=False)    
        else:   
            for i in range(len(curr_node.get_children())):
                if intent_ret == curr_node.get_children()[i].intent:
                    curr_user.currentnode=curr_node.get_children()[i]
                    curr_user.save()
                    return JsonResponse(curr_user.currentnode.message, safe=False)
            print('general_jose')
            return JsonResponse(curr_user.currentnode.message, safe=False)

        
