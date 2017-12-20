from django.db import models
from django.utils import timezone
from datetime import datetime
from Jobs.models import Jobs

class Scheduled_items(models.Model):
	description = models.CharField(max_length=100, default='')
	date_1 = models.DateField(default=timezone.now)
	date_2 = models.DateField(default=date_1)
	quantity = models.IntegerField(default=1)
	job = models.ForeignKey(Jobs, null=True) # RECOVER FKEY
	model = models.CharField(default='Scheduled_items', max_length=100)

class Purchase_orders(models.Model):
	id = models.AutoField(primary_key=True)
	supplier = models.CharField(max_length=100, default='')
	supplier_ref = models.CharField(max_length=100, default='')

	def __str__(self):
		return f'{self.id + 4000}'

class Items(models.Model):
	description = models.CharField(max_length=100, default='')
	fullname = models.CharField(max_length=100, default='')
	delivery_location = models.CharField(max_length=100, default='')
	price = models.DecimalField(default=1.00, decimal_places=2, max_digits=25)
	status = models.CharField(max_length=100, default='')
	order_date = models.CharField(max_length=100, default='')
	delivery_date = models.CharField(max_length=100, default='') #
	quantity = models.IntegerField(default=1)
	PO = models.ForeignKey(Purchase_orders, blank=True, null=True) # RECOVER FKEY
	job = models.ForeignKey(Jobs, blank=True, null=True) # RECOVER FKEY
	model = models.CharField(default='Items', max_length=100)

# Create your models here.
