from django.db import models


class Jobs(models.Model):
	name = models.CharField(max_length=100, default='')
	email = models.CharField(max_length=100, default='')
	phone = models.CharField(max_length=100, default='')
	address = models.CharField(max_length=100, default='')
	job_id = models.CharField(max_length=100, default='', unique=True)
	status = models.CharField(max_length=100, default='quote') # 'quote', 'ongoing' or 'completed'

	def __str__(self):
		return f'{self.address}'
	# have to manually query notes for all notes whose job foreign key is this job.
