from rest_framework import serializers
from book.models import Book, LANGUAGE_CHOICES


class BookSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Book
        fields = ('id', 'title', 'author', 'language', 'year')