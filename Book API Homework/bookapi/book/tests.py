# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from book.models import Book

class BookAPITests(APITestCase):

    """
	Tests the POST feature of the http://localhost:8000/book/.
	"""
    def test_booklist_post(self):
        url = reverse('book')
        data = {'title': 'exampletitle', 'author': 'exampleauthor', 'language': 'english'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 1)
        self.assertEqual(Book.objects.get().title, 'exampletitle')
        self.assertEqual(Book.objects.get().author, 'exampleauthor')
        self.assertEqual(Book.objects.get().language, 'english')