from django.db import models
from datetime import datetime
from django.utils import timezone

class Site_info(models.Model):
	locked = models.BooleanField(default=False) #false when site is locked
	password = models.CharField(max_length=150)

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

class Notes(models.Model):
	Title = models.CharField(max_length=100, default='')
	Text = models.CharField(max_length=100, default='')
	Timestamp = models.DateTimeField(auto_now_add=True)
	job = models.ForeignKey(Jobs, null=True)
	model = models.CharField(default='Notes', max_length=100)

	class Meta:
		ordering = ('-Timestamp',)

class Scheduled_items(models.Model):
	description = models.CharField(max_length=100, default='')
	date_1 = models.DateField(default=timezone.now)
	date_2 = models.DateField(default=date_1)
	quantity = models.IntegerField(default=1)
	job = models.ForeignKey(Jobs)
	model = models.CharField(default='Scheduled_items', max_length=100)

class Purchase_orders(models.Model):
	supplier = models.CharField(max_length=100, default='')
	supplier_ref = models.CharField(max_length=100, default='')
	order_no = models.AutoField(primary_key=True)


class Items(models.Model):
	description = models.CharField(max_length=100, default='')
	fullname = models.CharField(max_length=100, default='')
	delivery_location = models.CharField(max_length=100, default='')
	price = models.IntegerField(default=1)
	status = models.CharField(max_length=100, default='')
	order_date = models.CharField(max_length=100, default='')
	delivery_date = models.CharField(max_length=100, default='') #
	quantity = models.IntegerField(default=1)
	PO = models.ForeignKey(Purchase_orders, blank=True, null=True)
	job = models.ForeignKey(Jobs)
	model = models.CharField(default='Items', max_length=100)

class Shopping_list_items(models.Model):
	description = models.CharField(max_length=100, default='')
	quantity = models.IntegerField(default=1)
	job = models.ForeignKey(Jobs)
	model = models.CharField(default='Shopping_list_items', max_length=100)







# Create your models here.
