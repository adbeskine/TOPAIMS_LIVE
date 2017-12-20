from django.conf.urls import url
from .views import homepage

urlpatterns = [
	url(r'^$', homepage, name='homepage'),
]