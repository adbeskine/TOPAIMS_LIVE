from django.db import models
from Jobs.models import Jobs

class Shopping_list_items(models.Model):
	description = models.CharField(max_length=100, default='')
	quantity = models.IntegerField(default=1)
	job = models.ForeignKey(Jobs, null=True) # RECOVER FKEY
	model = models.CharField(default='Shopping_list_items', max_length=100)
