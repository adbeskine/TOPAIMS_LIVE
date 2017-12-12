
from .base import Test
from django.urls import reverse
from django.contrib import messages
from django.conf import settings
from home.models import Jobs, Notes, Site_info, Scheduled_items, Items, Purchase_orders, Shopping_list_items
import time
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

title_1 = 'JARVIS disturbing workers'
text_1 = "JARVIS keeps pestering the workers with 'suggestions', remind workers to be polite"
title_2 = 'JARVIS can read these notes'
text_2 = "JARVIS reminded our workers that we told them not to ignore him today... has he got nothing more interesting to do?"
now = settings.NOW
current_date = now
current_date_string = str(current_date.strftime('%Y/%d/%m'))
one_month_future = current_date + relativedelta(months=1)
one_month_future_string = str(one_month_future.strftime('%Y/%d/%m'))



class JobViewTest(Test):

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

class JobViewProfileTests(JobViewTest):

	#-- HELPER METHODS --#

	def update_job_status(self, job_id, status):
		response = self.client.get(reverse('update_job', kwargs={'status':status, 'job_id': job_id}), follow=True)
		self.assertRedirects(response, reverse('job', kwargs={'job_id': job_id}))
	#-- SETUP AND TEARDOWN --#
	def setUp(self):
		Site_info.objects.create(locked=False, password='thischangesautomaticallyaftereverylock')
		self.login()
		self.create_job()

	#------------------------#

	def test_job_data_in_context(self):
		# setup has landed already in job view
		response = self.client.get(reverse('job', kwargs={'job_id':'200ParkAvenue'}))
		job = Jobs.objects.filter(address='200 Park Avenue').first()
		self.assertEquals(response.context['job'], job)

	def test_job_status_changes(self):
		job = Jobs.objects.filter(address='200 Park Avenue').first()
		self.update_job_status(job.job_id, 'ongoing')
		job = Jobs.objects.filter(address='200 Park Avenue').first()
		self.assertEquals(job.status, 'ongoing')

		self.update_job_status(job.job_id, 'completed')
		job = Jobs.objects.filter(address='200 Park Avenue').first()
		self.assertEquals(job.status, 'completed')

		self.update_job_status(job.job_id, 'quote')
		job = Jobs.objects.filter(address='200 Park Avenue').first()
		self.assertEquals(job.status, 'quote')


class JobViewNotesTests(JobViewTest):

	#-- HELPER METHODS --#
	def create_note(self, title, text, job_id):
		response = self.client.post(reverse('new_note', kwargs={'job_id':job_id }), data={'Title':title, 'Text':text}, follow=True)
		self.assertRedirects(response, reverse('job', kwargs={'job_id':job_id}))
	#-- SETUP AND TEARDOWN --#
	def setUp(self):
		Site_info.objects.create(locked=False, password='thischangesautomaticallyaftereverylock')
		self.login()
		self.create_job()

	#------------------------#

	def test_note_creation(self):
		job = Jobs.objects.filter(address='200 Park Avenue').first()

		self.create_note(title_1, text_1, job.job_id) # titles and texts defined just under imports
		# redirect is asserted in the helper method
		
		job_notes = Notes.objects.filter(job=job).order_by('-Timestamp')

		self.assertEquals(job_notes[0].Title, title_1)
		self.assertEquals(job_notes[0].Text, text_1)

	def test_multiple_note_creation(self):
		job = Jobs.objects.filter(address='200 Park Avenue').first()
		time.sleep(2)
		self.create_note(title_1, text_1, job.job_id)
		time.sleep(2)
		self.create_note(title_2, text_2, job.job_id)

		job_notes = Notes.objects.filter(job=job).order_by('-Timestamp') #REFRACT can I use job_notes[0]?

		self.assertEquals(job_notes[0].Title, title_2) 
		self.assertEquals(job_notes[1].Title, title_1)
		self.assertEquals(job_notes[2].Title, 'First Note')



class JobViewScheduleOfItemsTest(JobViewTest):


	def setUp(self):
		Site_info.objects.create(locked=False, password='thischangesautomaticallyaftereverylock')
		self.login()
		self.create_job()

		#-- HELPER METHODS --#

	def create_schedule_item(self, description, date_1, quantity, job_id, date_2=None):
		if date_2:
			schedule_item_form_data = {
			'description':description,
			'date_1':date_1,
			'date_2':date_2,
			'quantity':quantity
			}
		elif date_2 == None:
			schedule_item_form_data = {
			'description':description,
			'date_1':date_1,
			'quantity':quantity
			}
		return self.client.post(reverse('new_schedule_item', kwargs={'job_id':job_id}), data = schedule_item_form_data, follow=True)


	def test_new_scheduled_item_creation_one_date(self):
		job = Jobs.objects.filter(address='200 Park Avenue').first()
		response = self.create_schedule_item('test item 1 description', current_date, 1, '200ParkAvenue')


		scheduled_item_1 = Scheduled_items.objects.filter(description='test item 1 description').first()

		self.assertRedirects(response, reverse('job', kwargs={'job_id':'200ParkAvenue'}))
		storage = messages.get_messages(response)
		for message in storage:
			self.assertEquals(message, "'test item 1 description' successfully scheduled for " + current_date_string)
		self.assertEquals(scheduled_item_1.description, 'test item 1 description')
		self.assertEquals(scheduled_item_1.date_1, current_date)
		self.assertEquals(scheduled_item_1.date_2, current_date)
		self.assertEquals(scheduled_item_1.quantity, 1)
		self.assertEquals(scheduled_item_1.job, job)

	def test_new_schedule_item_creation_date_range(self):
		job = Jobs.objects.filter(address='200 Park Avenue').first()
		response = self.create_schedule_item('test item 1 description', current_date, 1, '200ParkAvenue', one_month_future)
		scheduled_item_1 = Scheduled_items.objects.filter(description='test item 1 description').first()

		self.assertRedirects(response, reverse('job', kwargs={'job_id':'200ParkAvenue'}))
		storage = messages.get_messages(response)
		for message in storage:
			self.assertEquals(message, "'test item 1 description' successfully scheduled for " + current_date_string + '-' + one_month_future_string)
		self.assertEquals(scheduled_item_1.description, 'test item 1 description')
		self.assertEquals(scheduled_item_1.date_1, current_date)
		self.assertEquals(scheduled_item_1.date_2, one_month_future)
		self.assertEquals(scheduled_item_1.quantity, 1)
		self.assertEquals(scheduled_item_1.job, job)

	def test_schedule_item_update_date(self):
		self.create_schedule_item('test item 1 description', current_date, 1, '200ParkAvenue')
		scheduled_item_1 = Scheduled_items.objects.first()


		response=self.client.post(reverse('schedule_item', kwargs={'function':'update', 'pk':scheduled_item_1.pk}), data={'update_date_1':one_month_future})
		
		scheduled_item_1 = Scheduled_items.objects.get(pk=scheduled_item_1.pk)
		self.assertRedirects(response, reverse('job', kwargs={'job_id':'200ParkAvenue'}))
		self.assertEquals(scheduled_item_1.date_1, one_month_future)

		self.client.post(reverse('schedule_item', kwargs={'function':'update', 'pk':scheduled_item_1.pk}), data={'update_date_1':current_date, 'update_date_2':one_month_future})

		scheduled_item_1 = Scheduled_items.objects.get(pk=scheduled_item_1.pk)
		self.assertEquals(scheduled_item_1.date_1, current_date)
		self.assertEquals(scheduled_item_1.date_2, one_month_future)

	def test_schedule_item_delete(self):
		self.create_schedule_item('test item 1 description', current_date, 1, '200ParkAvenue')
		scheduled_item_1 = Scheduled_items.objects.first()

		response = self.client.post(reverse('schedule_item', kwargs={'function':'delete', 'pk':scheduled_item_1.pk}), data={'confirmed':True}, follow=True)

		self.assertEquals(Scheduled_items.objects.count(), 0)
		self.assertRedirects(response, reverse('job', kwargs={'job_id':'200ParkAvenue'}))

	def test_purchase_order(self): # REFRACT
		job = Jobs.objects.filter(address='200 Park Avenue').first()

		PO_data = {
		'Supplier':'Stark Industries',
		'Supplier_ref':'0001',
		'order_no': Purchase_orders.objects.count()+1, #I think? i.e, the next pk? # REFRACT, this is now an auto field in the model and is ignored in the view

		'item_1_description':'test item 1',
		'item_1_fullname':'test item 1 fullname',
		'item_1_delivery_location':('shop',),
		'item_1_price':100,
		'item_1_job':'200 Park Avenue',
		'item_1_delivery_date':one_month_future,
		'item_1_quantity':1,

		'item_2_description':'test item 2',
		'item_2_fullname':'test item 2 fullname',
		'item_2_delivery_location':('site',),
		'item_2_price':200,
		'item_2_job':'200 Park Avenue',
		'item_2_delivery_date':current_date,
		'item_2_quantity':2
		}

		response = self.client.post(reverse('purchase_order', kwargs={'job_id':'200ParkAvenue'}), data=PO_data, follow=True)


		self.assertEquals(Items.objects.count(), 2)

		self.assertRedirects(response, reverse('job', kwargs={'job_id':'200ParkAvenue'}))
		
		Items_item_1 = Items.objects.get(description='test item 1')
		Items_item_2 = Items.objects.get(description='test item 2')
		PO = Purchase_orders.objects.first()

		self.assertEquals(Items_item_1.PO, PO) # foreign key
		self.assertEquals(Items_item_1.description, 'test item 1')
		self.assertEquals(Items_item_1.fullname, 'test item 1 fullname')
		self.assertEquals(Items_item_1.delivery_location, 'shop')
		self.assertEquals(Items_item_1.price, 100)
		self.assertEquals(Items_item_1.job, job) # foreign key
		self.assertEquals(Items_item_1.delivery_date, one_month_future.strftime('%Y-%m-%d'))
		self.assertEquals(Items_item_1.status, 'ORDERED')
		self.assertEquals(Items_item_1.order_date, current_date.strftime('%Y-%m-%d'))
		self.assertEquals(Items_item_1.quantity, 1)

		self.assertEquals(Items_item_2.PO, PO) # foreign key
		self.assertEquals(Items_item_2.description, 'test item 2')
		self.assertEquals(Items_item_2.fullname, 'test item 2 fullname')
		self.assertEquals(Items_item_2.delivery_location, 'site')
		self.assertEquals(Items_item_2.price, 200)
		self.assertEquals(Items_item_2.job, job) # foreign key
		self.assertEquals(Items_item_2.delivery_date, current_date.strftime('%Y-%m-%d'))
		self.assertEquals(Items_item_2.status, 'ORDERED')
		self.assertEquals(Items_item_2.order_date, current_date.strftime('%Y-%m-%d'))
		self.assertEquals(Items_item_2.quantity, 2)

		self.assertEquals(PO.supplier, 'Stark Industries')
		self.assertEquals(PO.supplier_ref, '0001')
		self.assertEquals(PO.order_no, 1)

	def test_en_route_to_on_site(self):
		new_shopping_list_item_data = {
			'description':'acquired -> delivered item 1',
			'job':'200 Park Avenue',
			'quantity':1
		}
		self.client.post(reverse('shopping_list_create', kwargs={'function':'create'}), data=new_shopping_list_item_data, follow=True)
		shopping_list_item_1 = Shopping_list_items.objects.filter(description='acquired -> delivered item 1').first()
		self.client.get(reverse('acquired', kwargs={'pk':shopping_list_item_1.pk}))
		acquired_item_object = Items.objects.filter(description = 'acquired -> delivered item 1').first() # # REFRACT come up with a tidier way to get an en route acquired item

		self.client.get(reverse('mark_on_site', kwargs={'pk':acquired_item_object.pk}))

		acquired_item_object = Items.objects.filter(description = 'acquired -> delivered item 1').first()

		self.assertEquals(acquired_item_object.status, 'ON-SITE')




	
		







		






















