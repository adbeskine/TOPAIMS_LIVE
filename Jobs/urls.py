from django.conf.urls import url
from Jobs.views import new_job, jobs, delete_job, update_job

urlpatterns = [
	url(r'^new_job_form/$', new_job, name='new_job_form'),
    url(r'^jobs/$', jobs, name='jobs'),
    url(r'^update_job/(?P<job_id>.+?)/(?P<status>.+?)/$', update_job, name='update_job'),
    url(r'^delete/$', delete_job, name='delete_job'),
]