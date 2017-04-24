from django.conf.urls import url, include 
from book import views

urlpatterns = [
    url(r'^', include(book.urls)),    
]
