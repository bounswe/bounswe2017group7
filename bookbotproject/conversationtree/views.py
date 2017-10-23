# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from conversationtree.models import Node
from serializers import NodeSerializer

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
