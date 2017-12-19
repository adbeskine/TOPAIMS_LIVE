from django.conf.urls import url 
from Shopping_list.views import shopping_list

urlpatterns = [
	url(r'^shopping_list/$', shopping_list, name='shopping_list'),
    url(r'^shopping_list/(?P<function>.+?)/$', shopping_list, name='shopping_list_create'),
]