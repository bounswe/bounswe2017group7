"""bookbotproject URL Configuration

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
from django.contrib import admin
from conversationtree import views as tree_views
from home_page import views as home_views
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^nodes/$', views.node_list),
    url(r'^nodes/(?P<pk>\w+)/$', views.nodes_detail),
    url(r'^getUser/(?P<pk>\w+)/$', views.get_user_info),
    url(r'^addUser/(?P<_name>\w+)/(?P<_userid>\w+)/(?P<_chatid>\w+)/$', views.add_new_user),
    url(r'^getResponse/(?P<_message>[\w ]+)/(?P<_chatid>[\w ]+)/$', views.get_response)
]
