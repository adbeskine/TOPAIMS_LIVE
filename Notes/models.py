from django.db import models
from Jobs.models import Jobs

class Notes(models.Model):
	Title = models.CharField(max_length=100, default='')
	Text = models.TextField(default='')
	Timestamp = models.DateTimeField(auto_now_add=True)
	job = models.ForeignKey(Jobs, null=True) # RECOVER FKEY
	model = models.CharField(default='Notes', max_length=100)

	class Meta:
		ordering = ('-Timestamp',)