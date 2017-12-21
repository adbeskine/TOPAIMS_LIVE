from .base import Test
from django.urls import reverse
from django.conf import settings

from _Auth.models import Site_info
from Jobs.models import Jobs
from Notes.models import Notes
from Item_Flow.models import Scheduled_items, Purchase_orders, Items
from Shopping_list.models import Shopping_list_items


class DeletesTest(Test):

	# this test is the urls which delete: job notes, admin notes, acquired shopping list items, PO items, shopping list items, jobs

	#-- HELPER METHODS --#

	def create_custom_job(self, name, email, phone, address, note):
		form_data = {
		'Name':name,
		'Email':email,
		'Phone':phone,
		'Address':address,
		'Note':note,
		}

		response = self.client.post(reverse('new_job_form'), form_data, follow=True)
	
	def create_shopping_list_item(self, description, quantity, job):

  		new_shopping_list_item_data = {
  			'description':description,
  			'job':job.address,
  			'quantity':1
  		}
  		self.client.post(reverse('shopping_list_create', kwargs={'function':'create'}), data=new_shopping_list_item_data, follow=True)
	
	def create_acquired_shopping_list_item(self, description, quantity, job):

		self.create_shopping_list_item(description, quantity, job)
		shopping_list_item = Shopping_list_items.objects.filter(description=description).first()
		self.client.get(reverse('acquired', kwargs={'pk':shopping_list_item.pk}), follow=True)

	def create_purchase_order(
		self, Supplier='Strark Industries', Supplier_ref='123',
		description1=None, fullname1=None, delivery_date1=None, quantity1=None, price1=None, job1=None, delivery_location1=None,
		description2=None, fullname2=None, delivery_date2=None, quantity2=None, price2=None, job2=None, delivery_location2=None,
		description3=None, fullname3=None, delivery_date3=None, quantity3=None, price3=None, job3=None, delivery_location3=None,
		description4=None, fullname4=None, delivery_date4=None, quantity4=None, price4=None, job4=None, delivery_location4=None,
		description5=None, fullname5=None, delivery_date5=None, quantity5=None, price5=None, job5=None, delivery_location5=None,
		description6=None, fullname6=None, delivery_date6=None, quantity6=None, price6=None, job6=None, delivery_location6=None,
		description7=None, fullname7=None, delivery_date7=None, quantity7=None, price7=None, job7=None, delivery_location7=None,
		description8=None, fullname8=None, delivery_date8=None, quantity8=None, price8=None, job8=None, delivery_location8=None,
		description9=None, fullname9=None, delivery_date9=None, quantity9=None, price9=None, job9=None, delivery_location9=None,
		description10=None, fullname10=None, delivery_date10=None, quantity10=None, price10=None, job10=None, delivery_location10=None,
		):
		
		PO_data = {
		'Supplier':Supplier,
		'Supplier_ref':Supplier_ref,
		'item_1_description':description1,
		'item_1_fullname':fullname1,
		'item_1_delivery_location':(delivery_location1,),
		'item_1_job':job1.address,
		'item_1_delivery_date':delivery_date1, #must be date object.
		'item_1_quantity':quantity1,
		'item_1_price':price1,
		}

		if description2:
			PO_data.update({
				'item_2_description':description2,
				'item_2_fullname':fullname2,
				'item_2_delivery_location':(delivery_location2,),
				'item_2_job':job2.address,
				'item_2_delivery_date':delivery_date2, #must be date object.
				'item_2_quantity':quantity2,
				'item_2_price':price2,
					})

		if description3:
			PO_data.update({
				'item_3_description':description3,
				'item_3_fullname':fullname3,
				'item_3_delivery_location':(delivery_location3,),
				'item_3_job':job3.address,
				'item_3_delivery_date':delivery_date3, #must be date object.
				'item_3_quantity':quantity3,
				'item_3_price':price3,
					})

		if description4:
			PO_data.update({
				'item_4_description':description4,
				'item_4_fullname':fullname4,
				'item_4_delivery_location':(delivery_location4,),
				'item_4_job':job4.address,
				'item_4_delivery_date':delivery_date4, #must be date object.
				'item_4_quantity':quantity4,
				'item_4_price':price4,
					})

		if description5:
			PO_data.update({
				'item_5_description':description5,
				'item_5_fullname':fullname5,
				'item_5_delivery_location':(delivery_location5,),
				'item_5_job':job5.address,
				'item_5_delivery_date':delivery_date5, #must be date object.
				'item_5_quantity':quantity5,
				'item_5_price':price5,
					})

		if description6:
			PO_data.update({
				'item_6_description':description6,
				'item_6_fullname':fullname6,
				'item_6_delivery_location':(delivery_location6,),
				'item_6_job':job6.address,
				'item_6_delivery_date':delivery_date6, #must be date object.
				'item_6_quantity':quantity6,
				'item_6_price':price6,
					})

		if description7:
			PO_data.update({
				'item_7_description':description7,
				'item_7_fullname':fullname7,
				'item_7_delivery_location':(delivery_location7,),
				'item_7_job':job7.address,
				'item_7_delivery_date':delivery_date7, #must be date object.
				'item_7_quantity':quantity7,
				'item_7_price':price7,
					})

		if description8:
			PO_data.update({
				'item_8_description':description8,
				'item_8_fullname':fullname8,
				'item_8_delivery_location':(delivery_location8,),
				'item_8_job':job8.address,
				'item_8_delivery_date':delivery_date8, #must be date object.
				'item_8_quantity':quantity8,
				'item_8_price':price8,
					})

		if description9:
			PO_data.update({
				'item_9_description':description9,
				'item_9_fullname':fullname9,
				'item_9_delivery_location':(delivery_location9,),
				'item_9_job':job9.address,
				'item_9_delivery_date':delivery_date9, #must be date object.
				'item_9_quantity':quantity9,
				'item_9_price':price9,
					})

		if description10:
			PO_data.update({
				'item_10_description':description10,
				'item_10_fullname':fullname10,
				'item_10_delivery_location':(delivery_location10,),
				'item_10_job':job10.address,
				'item_10_delivery_date':delivery_date10, #must be date object.
				'item_10_quantity':quantity10,
				'item_10_price':price10,
					})

		self.client.post(reverse('purchase_order_homepage'), data=PO_data, follow=True)
	
	def create_job_note(self, title, text, job):
		note_form_data = {
			'Title':title,
			'Text':text
		}
		self.client.post(reverse('new_note', kwargs={'job_id':job.job_id}), data=note_form_data, follow=True)
	
	def create_admin_note(self, title, text):
		note_form_data = {
			'Title':title,
			'Text':text
		}
		self.client.post(reverse('new_note', kwargs={'job_id':'admin'}), data=note_form_data, follow=True)

	def create_schedule_item(self, description, date_1, quantity, job, date_2=None):
		
		if date_2:	
			schedule_item_form_data = {
				'description':description,
				'date_1':date_1,
				'date_2':date_2,
				'quantity':quantity
				}

			return self.client.post(reverse('new_schedule_item', kwargs={'job_id':job.job_id}), data=schedule_item_form_data, follow=True)

		else:
			schedule_item_form_data = {
				'description':description,
				'date_1':date_1,
				'quantity':quantity
				}

			return self.client.post(reverse('new_schedule_item', kwargs={'job_id':job.job_id}), data=schedule_item_form_data, follow=True)

	#-- SETUP AND TEARDOWN --#
	# Job 1: # all of these are plus one so as to differentiate between the whole job deletion and the manual deletes #job 1 for manual deletes, job 2 will be totally deleted
		# 2 shopping list items # make sure only one is deleted in unittests 
		# 2 acquired shopping list item (item with no P.O)
		# 2 purchase order item # make sure only one is deleted in unittests
		# 2 Job notes (one to delete and one to compare against)

	# Job 2:
		# 3 shopping list items
		# 3 acquired shopping list items
		# 3 Scheduled item
		# purchase order no.1:
			# 3 Purchase Order items
		# purchase order no.2:
			# 3 Purchase Order items
		# 3 Note

	# extras:
		# 2 admin notes

	def setUp(self):
		now = settings.NOW
		self.setup_system()
		self.login()

		# Job 1
		self.create_custom_job(name='Tony Stark', email='Tony@StarkIndustries.net', phone='01234567898', address='200 Park Avenue', note='this is job 1')
		job1 = Jobs.objects.filter(address='200 Park Avenue').first()

		# shopping list items 1 and 2
		self.create_shopping_list_item('job 1 shopping list item 1', 1, job1)
		self.create_shopping_list_item('job 1 shopping list item 2', 1, job1)

		# acquired shopping list items 1 and 2
		self.create_acquired_shopping_list_item('job 1 acquired shopping list item 1', 1, job1)
		self.create_acquired_shopping_list_item('job 1 acquired shopping list item 2', 1, job1)

		# purchase order with 2 items
		self.create_purchase_order(
			description1='job 1 purchase order 1 item 1 description',
			fullname1='job 1 purchase order 1 item 1 fullname',
			delivery_date1=now,
			quantity1=1,
			price1=100,
			job1=job1,
			delivery_location1='shop',

			description2='job 1 purchase order 1 item 2 description',
			fullname2='job 1 purchase order 1 item 2 fullname',
			delivery_date2=now,
			quantity2=1,
			price2=100,
			job2=job1,
			delivery_location2='shop',
			)

		# Job notes 1 and 2
		self.create_job_note('job 1 note 1 title', 'job 1 note 1 text', job1)
		self.create_job_note('job 1 note 2 title', 'job 1 note 2 text', job1)



		# Job 2
		self.create_custom_job(name='Adam Jensen', email='Adam.Jensen@si.det.usa', phone='01234567898', address='601 Chiron Building', note='this is job 2')
		job2 = Jobs.objects.filter(address='601 Chiron Building').first()

		# Job 2 shopping list items 1-3
		self.create_shopping_list_item('job 2 shopping list item 1', 1, job2)
		self.create_shopping_list_item('job 2 shopping list item 2', 1, job2)
		self.create_shopping_list_item('job 2 shopping list item 3', 1, job2)

		# Job 2 acquired shopping list items 1-3
		self.create_acquired_shopping_list_item('job 2 acquired shopping list item 1', 1, job2)
		self.create_acquired_shopping_list_item('job 2 acquired shopping list item 2', 1, job2)
		self.create_acquired_shopping_list_item('job 2 acquired shopping list item 3', 1, job2)

		# Job 2 Scheduled Items 1-3
		self.create_schedule_item('job 2 schedule item 1', now, 1, job2)
		self.create_schedule_item('job 2 schedule item 2', now, 1, job2)
		self.create_schedule_item('job 2 schedule item 3', now, 1, job2)


		# Job 2 Purchase order 1 with 3 items
		self.create_purchase_order(
			Supplier_ref = 'job 2 po 1',
			description1='job 2 purchase order 1 item 1 description',
			fullname1='job 2 purchase order 1 item 1 fullname',
			delivery_date1=now,
			quantity1=1,
			price1=100,
			job1=job2,
			delivery_location1='shop',

			description2='job 2 purchase order 1 item 2 description',
			fullname2='job 2 purchase order 1 item 2 fullname',
			delivery_date2=now,
			quantity2=1,
			price2=100,
			job2=job2,
			delivery_location2='shop',
			
			description3='job 2 purchase order 1 item 3 description',
			fullname3='job 2 purchase order 1 item 3 fullname',
			delivery_date3=now,
			quantity3=1,
			price3=100,
			job3=job2,
			delivery_location3='shop',
			)

		# Job 2 purchase order 2 with 3 items
		self.create_purchase_order(
			Supplier_ref = 'job 2 po 2',
			description1='job 2 purchase order 2 item 1 description',
			fullname1='job 2 purchase order 2 item 1 fullname',
			delivery_date1=now,
			quantity1=1,
			price1=100,
			job1=job2,
			delivery_location1='shop',

			description2='job 2 purchase order 2 item 2 description',
			fullname2='job 2 purchase order 2 item 2 fullname',
			delivery_date2=now,
			quantity2=1,
			price2=100,
			job2=job2,
			delivery_location2='shop',
			
			description3='job 2 purchase order 2 item 3 description',
			fullname3='job 2 purchase order 2 item 3 fullname',
			delivery_date3=now,
			quantity3=1,
			price3=100,
			job3=job2,
			delivery_location3='shop',
			)

		# Job 2 notes 1-3
		self.create_job_note('job 2 note 1 title', 'job 1 note 1 text', job2)
		self.create_job_note('job 2 note 2 title', 'job 1 note 2 text', job2)
		self.create_job_note('job 2 note 3 title', 'job 1 note 3 text', job2)

		# 2 Admin notes
		self.create_admin_note('admin note 1 title', 'admin note 1 text')
		self.create_admin_note('admin note 2 title', 'admin note 2 text')

	################################################################################################################################################################
	################################################################################################################################################################
	################################################################################################################################################################
	################################################################################################################################################################
	################################################################################################################################################################
	################################################################################################################################################################
	################################################################################################################################################################
	################################################################################################################################################################

	def test_all_deletes(self):

		# DELETING A SHOPPING LIST ITEM
		shopping_list_item_to_delete = Shopping_list_items.objects.filter(description = 'job 1 shopping list item 1').first()
		before_delete_count = Shopping_list_items.objects.count()

		self.client.get(reverse('delete', kwargs={'model':shopping_list_item_to_delete.model, 'pk':shopping_list_item_to_delete.pk}), follow=True)

		after_delete_count = Shopping_list_items.objects.count()
		self.assertEquals(after_delete_count, before_delete_count-1) # only the one item was deleted
		self.assertFalse(Shopping_list_items.objects.filter(pk=shopping_list_item_to_delete.pk).exists())


		# DELETING AN ACQUIRED SHOPPING LIST ITEM
		acquired_shopping_list_item_to_delete = Items.objects.filter(description='job 1 acquired shopping list item 1').first()
		before_delete_count = Items.objects.count()

		self.client.get(reverse('delete', kwargs={'model':acquired_shopping_list_item_to_delete.model, 'pk':acquired_shopping_list_item_to_delete.pk}), follow=True)

		after_delete_count = Items.objects.count()
		self.assertEquals(after_delete_count, before_delete_count-1)
		self.assertFalse(Items.objects.filter(pk=acquired_shopping_list_item_to_delete.pk).exists())


		# DELETING PURCHASE ORDER ITEM
		purchase_order_item_to_delete = Items.objects.filter(description='job 1 purchase order 1 item 1 description').first()
		before_delete_count = Items.objects.count()

		self.client.get(reverse('delete', kwargs={'model':purchase_order_item_to_delete.model, 'pk':purchase_order_item_to_delete.pk}), follow=True) # REFRACT - one method for this line amongst all objects to delete?

		after_delete_count = Items.objects.count()
		self.assertEquals(after_delete_count, before_delete_count-1)
		self.assertFalse(Items.objects.filter(pk=purchase_order_item_to_delete.pk).exists())


		# DELETE JOB NOTE
		job_note_to_delete = Notes.objects.filter(Title='job 1 note 1 title').first()
		before_delete_count = Notes.objects.count()

		self.client.get(reverse('delete', kwargs={'model':job_note_to_delete.model, 'pk':job_note_to_delete.pk}), follow=True)

		after_delete_count = Notes.objects.count()
		self.assertEquals(after_delete_count, before_delete_count-1)
		self.assertFalse(Notes.objects.filter(pk=job_note_to_delete.pk).exists())


		# DELETE ADMIN NOTE
		admin_note_to_delete = Notes.objects.filter(Title='admin note 1 title').first()
		before_delete_count = Notes.objects.count()

		self.client.get(reverse('delete', kwargs={'model':admin_note_to_delete.model, 'pk':admin_note_to_delete.pk}), follow=True)

		after_delete_count = Notes.objects.count()
		self.assertEquals(after_delete_count, before_delete_count-1)
		self.assertFalse(Notes.objects.filter(pk=admin_note_to_delete.pk).exists())


		
		# DELETE ENTIRE JOB

		before_delete_jobs_count = Jobs.objects.count()
		before_delete_shopping_list_items_count = Shopping_list_items.objects.count()
		before_delete_Items_items_count = Items.objects.count() # REMEMBER - this includes purchase order items and acquired shopping list items

		before_delete_notes_count = Notes.objects.count()
		before_delete_schedule_items_count = Scheduled_items.objects.count()

		job_to_delete = Jobs.objects.filter(address='601 Chiron Building') # REFRACT - instead of listing these out make it a proper db query?
		shopping_list_items_to_delete = [
			Shopping_list_items.objects.filter(description='job 2 shopping list item 1'),
			Shopping_list_items.objects.filter(description='job 2 shopping list item 2'),
			Shopping_list_items.objects.filter(description='job 2 shopping list item 3')
			]
		Acquired_items_to_delete = [
			Items.objects.filter(description='job 2 acquired shopping list item 1'),
			Items.objects.filter(description='job 2 acquired shopping list item 2'),
			Items.objects.filter(description='job 2 acquired shopping list item 3'),
			]

		Purchase_order_items_to_preserve = [
			Items.objects.filter(fullname='job 2 purchase order 1 item 1 fullname'),
			Items.objects.filter(fullname='job 2 purchase order 1 item 2 fullname'),
			Items.objects.filter(fullname='job 2 purchase order 1 item 3 fullname'),

			Items.objects.filter(fullname='job 2 purchase order 2 item 1 fullname'),
			Items.objects.filter(fullname='job 2 purchase order 2 item 2 fullname'),
			Items.objects.filter(fullname='job 2 purchase order 2 item 3 fullname'),
			]
		Purchase_orders_to_preserve = [
			Purchase_orders.objects.filter(supplier_ref='job 2 po 1'),
			Purchase_orders.objects.filter(supplier_ref='job 2 po 2'),
			]
		Notes_items_to_delete = [
			Notes.objects.filter(Title='job 2 note 1 title'),
			Notes.objects.filter(Title='job 2 note 2 title'),
			Notes.objects.filter(Title='job 2 note 3 title')
			]

		Schedule_items_items_to_delete=[
			Scheduled_items.objects.filter(description='job 2 schedule item 1'),
			Scheduled_items.objects.filter(description='job 2 schedule item 2'),
			Scheduled_items.objects.filter(description='job 2 schedule item 3')
			]
		
		job_delete_form_data = {
			'job_deletion_selection':('601 Chiron Building',),
			'security_field_1':'601 Chiron Building',
			'security_field_2':'601 Chiron Building'
				}

		
		self.client.post(reverse('delete_job'), data=job_delete_form_data, follow=True) # different url NAME for delete view function with no url arguments
		
		after_delete_jobs_count = Jobs.objects.count()
		after_delete_shopping_list_items_count = Shopping_list_items.objects.count()
		after_delete_Items_items_count = Items.objects.count() # REMEMBER - this includes purchase order items and acquired shopping list items
		after_delete_notes_count = Notes.objects.count()
		after_delete_schedule_items_count = Scheduled_items.objects.count()

		self.assertEquals(after_delete_jobs_count, before_delete_jobs_count-1)
		self.assertEquals(after_delete_shopping_list_items_count, before_delete_shopping_list_items_count-3)
		self.assertEquals(after_delete_Items_items_count, before_delete_Items_items_count-3) # 3 acquired items deleted, 6 po items preserved for purchase order
		self.assertEquals(after_delete_schedule_items_count, before_delete_schedule_items_count-3)
		self.assertEquals(after_delete_notes_count, before_delete_notes_count-4) #4th note is note generated upon creation of job

		self.assertFalse(job_to_delete.exists())
		for item in shopping_list_items_to_delete: # REFRACT - put all these for loops in to one 'for item in shopping_list... , items_items.... ,'?
			self.assertFalse(item.exists())
		for item in Acquired_items_to_delete:
			self.assertFalse(item.exists())
		for item in Notes_items_to_delete:
			self.assertFalse(item.exists())
		for item in Schedule_items_items_to_delete:
			self.assertFalse(item.exists())

		for item in Purchase_orders_to_preserve:
			self.assertTrue(item.exists())
		for item in Purchase_order_items_to_preserve:
			self.assertTrue(item.exists())










