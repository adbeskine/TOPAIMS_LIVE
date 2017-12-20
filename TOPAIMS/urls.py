"""TOPAIMS URL Configuration

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
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('Home_Panel.urls')),
    url(r'^', include('Jobs_Panel.urls')),
    url(r'^', include('_Auth.urls')),
    url(r'^', include('Item_Flow.urls')),
    url(r'^', include('Jobs.urls')),
    url(r'^', include('Notes.urls')),
    url(r'^', include('Shopping_list.urls')),
]
