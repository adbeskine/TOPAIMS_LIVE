from django.conf.urls import url
from _Auth.views import login, unlock

urlpatterns = [
	url(r'^login/$', login, name='login'),
	url(r'^unlock/(?P<unlock_password>.+?)/$', unlock, name='unlock'),
]