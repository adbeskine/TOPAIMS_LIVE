from django.conf.urls import url
from Jobs_Panel.views import job

urlpatterns=[
	url(r'^job/(?P<job_id>.+?)/$', job, name='job'),
]