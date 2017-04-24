"""bookapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from book import views

urlpatterns = [
    url(r'^book/$', views.book_list),
    url(r'^book/(?P<pk>[0-9]+)/$', views.book_detail),
    url(r'^book/(?P<title>[a-zA-Z0-9_\x20]+)/$', views.book_detail_by_title),
    url(r'^lang/(?P<lang>[a-zA-Z0-9_\x20]+)/$', views.book_detail_by_language),
]
