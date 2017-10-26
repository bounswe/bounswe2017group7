# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from conversationtree.models import Node
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
        node = Node.objects.get(intent="get-info")
    except Node.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'POST':
        newUser = TelegramUser.objects.create(name=_name, userid=_userid, chatid = _chatid, currentnode = node)
        return HttpResponse(status=200)



@csrf_exempt
def get_response(request, _message, _chatid):
    """ waits until a response from wit ai, it may take so much time !!!!"""

    if request.method == 'GET':
        intent_ret = None
        while intent_ret == None :
            intent_ret = get_Intent(_message)

        curr_user = TelegramUser.objects.get(chatid=_chatid)
        curr_node = curr_user.currentnode

        print(intent_ret)
        print(curr_node)

        for i in range(len(curr_node.get_children())):
            print("intent" + intent_ret)
            print(curr_node.get_children()[i].intent)
            if intent_ret == curr_node.get_children()[i].intent:
                curr_user.currentnode=curr_node.get_children()[i]
                curr_user.save()
                print("here")
                return JsonResponse(curr_user.currentnode.message, safe=False)

    return JsonResponse(curr_user.currentnode.message, safe=False)

    
