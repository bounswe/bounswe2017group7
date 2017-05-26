from rest_framework import serializers
from book.models import Book, LANGUAGE_CHOICES
from book.models import Author

class BookSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Book
        fields = ('id', 'title', 'author', 'language', 'year')


class AuthorSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Author
        fields = ('id', 'name', 'surname', 'age')
