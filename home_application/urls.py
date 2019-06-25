# -*- coding: utf-8 -*-
"""testapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url

from home_application import views

urlpatterns = (
    url(r'^$', views.home),
    url(r'helloworld', views.helloworld),
    url(r'HelloBlueking', views.HelloBlueking),
    url(r'addhost', views.addhost, name="addhost"),
    url(r'get-data', views.api_data, name="api-data"),
    url(r'show_data/(?P<pk>[0-9]+)', views.showdata.as_view(), name="showdata"),
    url(r'quickshow', views.quickshow, name="quickshow"),
    url(r'api/get_dfusage_hsq/$', views.api_disk_usage, name="api-quickshow"),
    url(r'get_usage_data/$', views.get_usage_data,name="get_usage_data"),
    url(r'importdata/$', views.importdata),


)
