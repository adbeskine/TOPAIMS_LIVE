from django.db import models

class Site_info(models.Model):
	locked = models.BooleanField(default=False) #false when site is locked
	password = models.CharField(max_length=150)

class Pass(models.Model):
	password = models.CharField(max_length=150, unique=True)
	user = models.CharField(max_length=150, unique=True) # a user MUST be either 'staff', 'manager' or 'super'
# Create your models here.
