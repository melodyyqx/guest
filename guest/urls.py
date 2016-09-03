"""guest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from sign.views import index
from sign.views import login_action
from sign.views import logout
from sign.views import event_manage,guest_manage,search_name,search_phone,sign_index,sign_index_action
from sign.views import add_event





urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^index/', index),
    url(r'^login_action/', login_action),
    url(r'^logout/',logout),
    url(r'^event_manage/',event_manage),
    url(r'^search_name/',search_name),
    url(r'^guest_manage/',guest_manage),
    url(r'^search_phone/',search_phone),
    url(r'^sign_index/(?P<event_id>[0-9]+)/$', sign_index),
    url(r'^sign_index_action/(?P<event_id>[0-9]+)/$', sign_index_action),
    url(r'^add_event/',add_event),
]