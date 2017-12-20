from .base import Test
from django.urls import reverse
from django.contrib import messages
from django.conf import settings
from home.models import Jobs, Notes, Site_info, Scheduled_items, Items, Purchase_orders, Shopping_list_items
import time
from datetime import datetime, timedelta

class ShoppingListTest(Test):

	#- HELPER METHODS -#
	def create_job(self):
		form_data = {
		'Name':'Tony Stark',
		'Email':'Tony@StarkIndustries.net',
		'Phone':'01234567899',
		'Address':'200 Park Avenue',
		'Note':"don't ignore JARVIS, he's temperemental and finds it rude",
		}

		response = self.client.post(reverse('new_job_form'), form_data, follow=True)

	#- SETUP AND TEARDOWN -#
	def setUp(self):
		Site_info.objects.create(locked=False, password='thischangesautomaticallyaftereverylock')
		self.login()
		self.create_job()


  #-------------------------------------------------------------------------------------------------------------------------#

	def test_shopping_list_page(self):

  		response = self.client.get(reverse('shopping_list'))
  		self.assertTemplateUsed(response, 'home/shopping_list.html')

	def test_shopping_list_CRUD(self):

  		job = Jobs.objects.filter(job_id='200ParkAvenue').first()

  		new_shopping_list_item_data = {
  			'description':'shopping list item 1',
  			'job':'200 Park Avenue',
  			'quantity':1
  		}
  		self.client.post(reverse('shopping_list_create', kwargs={'function':'create'}), data=new_shopping_list_item_data, follow=True)

  		
  		shopping_list_item_1 = Shopping_list_items.objects.filter(description='shopping list item 1').first()
  		self.assertEquals(shopping_list_item_1.description, 'shopping list item 1')
  		self.assertEquals(shopping_list_item_1.job, job)
  		self.assertEquals(shopping_list_item_1.quantity, 1)

  		
  		self.client.get(reverse('acquired', kwargs={'pk':shopping_list_item_1.pk}))

  		self.assertEquals(Shopping_list_items.objects.count(), 0)
  		
  		acquired_item_1 = Items.objects.filter(description='shopping list item 1').first()
  		self.assertEquals(acquired_item_1.description, 'shopping list item 1')
  		self.assertEquals(acquired_item_1.fullname, 'shopping list item 1')
  		self.assertEquals(acquired_item_1.status, 'ACQUIRED')
  		self.assertEquals(acquired_item_1.quantity, 1)
  		self.assertEquals(acquired_item_1.job, job)


