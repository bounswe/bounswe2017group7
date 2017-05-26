# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from book.models import Book
from book.models import Author

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

    def test_booksearch_language(self):
        """
        Dummy entries to database
        """
        url = reverse('book')
        data = {'title': 'dummy1', 'author': 'author1', 'language': 'turkish'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = {'title': 'dummy2', 'author': 'author2', 'language': 'english'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = {'title': 'dummy3', 'author': 'author3', 'language': 'english'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Test get functionality for 'english'
        url = reverse('search_language', kwargs={'lang': 'english'})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)
        response = json.loads(response.content)
        for book in response:
            self.assertEqual(book['language'], 'english')
        

    def test_authorlist_post(self):
        url = reverse('list_authors')
        data = {'name': 'examplename', 'surname': 'examplesur', 'age': '45'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Author.objects.count(), 1)
        self.assertEqual(Author.objects.get().name, 'examplename')
        self.assertEqual(Author.objects.get().surname, 'examplesur')
        self.assertEqual(Author.objects.get().age, '45')

