# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from book.models import Book
from book.serializers import BookSerializer

# Returns a Json response containing all the books.
@csrf_exempt
def book_list(request):
    """
    List all books, or create a new book.
    """
    if request.method == 'GET':
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = BookSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

# Returns a Json response for the book of id pk if the request is a GET request.
# Adds a new book to the database if the request is a PUT request.
# Deletes book of id pk if the request is a DELETE request.
@csrf_exempt
def book_detail(request, pk):
    """
    Retrieve, update or delete a book.
    """
    try:
        book = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = BookSerializer(book)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = BookSerializer(book, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        book.delete()
        return HttpResponse(status=204)

# Returns a Json response for the book of title if the request is a GET request.
# Adds a new book to the database if the request is a PUT request.
# Deletes book of title if the request is a DELETE request.
@csrf_exempt
def book_detail_by_title(request, title):
    """
    Retrieve, update or delete a book.
    """
    try:
        book = Book.objects.get(title=title)
    except Book.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = BookSerializer(book)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = BookSerializer(book, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        book.delete()
        return HttpResponse(status=204)


# Returns a Json response for the book in a given language if the request is a GET request.
# Adds a new book to the database if the request is a PUT request.
# Deletes book of title if the request is a DELETE request.
@csrf_exempt
def book_detail_by_language(request, lang):
    """
    Retrieve, update or delete a book.
    """

    print "hey"

    try:
        # Filters books
        book = Book.objects.filter(language = lang)
    except Book.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = BookSerializer(book, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = BookSerializer(book, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        book.delete()
        return HttpResponse(status=204)


def book_detail_by_author(request, author):
    """
    Retrieve, update or delete a book.
    """
    try:
        book = Book.objects.get(author=author)
    except Book.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = BookSerializer(book,many=True)
        return JsonResponse(serializer.data,safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = BookSerializer(book, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        book.delete()
        return HttpResponse(status=204)



