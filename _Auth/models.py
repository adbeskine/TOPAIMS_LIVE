from django.db import models

class Site_info(models.Model):
	locked = models.BooleanField(default=False) #false when site is locked
	password = models.CharField(max_length=150)
# Create your models here.
