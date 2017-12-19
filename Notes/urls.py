from django.conf.urls import url
from Notes.views import new_note

urlpatterns=[
	url(r'^new_note/(?P<job_id>.+?)/$', new_note, name='new_note'),
]