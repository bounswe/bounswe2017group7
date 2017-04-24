from django.conf.urls import url
from book import views

urlpatterns = [
    url(r'^book/$', views.book_list),
]