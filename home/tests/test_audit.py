# the audit table has five columns: action, object, user, date, time
# whenever a cud action is performed a post request will be sent to /audit with url parameters which give the action, table, pkey, description, user, date, time

import time
from datetime import date
from dateutil.relativdelta import relativdelta

from .base import Test
from django.urls import reverse
from django.conf import settings

from _Auth.models import Site_info
from audit.models import Audit
from Jobs.models import Jobs
from Notes.models import Notes
from Item_Flow.models import Scheduled_items, Purchase_orders
from Shopping_list.models import Shopping_list_items

# obviously this will be put into one whole class next.
from home.unittest_helper_methods import create_custom_job, create_schedule_item, create_purchase_order, create_shopping_list_item, create_admin_note, create_job_note
from home.unittest_helper_methods import mark_showroom, mark_on_site, create_purchase_order_item, reject_and_reschedule, reject_and_cancel, create_acquired_shopping_list_item
from home.unittest_helper_methods import delete_job, delete_schedule_item, delete_shopping_list_item, delete_acquired_shopping_list_item, delete_note
#-- CREATES --#

class AuditTest(Test):

	#-- HELPER METHODS --#

	def find_audit_object(relevant_object, action):
		return Audit.objects.filter(pkey=relevant_object.pk, table=relevant_object._meta.db_table, action=action).first()

	#-- SETUP AND TEARDOWN --#

	def setUp(self):
		self.setup_system()
		self.loginSuper()
		self.create_custom_job(name='base test job', email='asdf@asdf.com', phone='01234567898', address='10 basejob road', note='asdf')

	#-------------------------------------------------------------------------------------------------------------------------------------#


	def test_create_job(self): # when a job is created appropriate audit update occurs
		time = strftime("%H:%M")
		self.create_custom_job(name='testjob1', email='asdf@asdf.com', phone='01234567898', address='10 testjob road', note='asdf')
		time2 = strftime("%H:%M")

		new_job = Jobs.objects.filter(address='10 testjob road').first()
		new_audit_object = find_audit_object(new_job, 'CREATE')

		self.assertEquals(new_audit_object.action, 'CREATE')
		self.assertEquals(new_audit_object.table, 'Jobs_jobs')
		self.assertEquals(new_audit_object.pkey, new_job.pk)
		self.assertEquals(new_audit_object.description, f'{new_job.address} job profile created')
		self.assertEquals(new_audit_object.user, 'super')
		self.assertEquals(new_audit_object.date, settings.NOW)
		if time == time2:
			self.assertEquals(new_audit_object.time, time)
		else:
			self.assertEquals(new_audit_object.time, time2)

	def test_create_schedule_item_super(self):
		time = strftime("%H:%M")
		self.create_schedule_item(description='test schedule item super', date_1=settings.NOW, quantity=1, job=Jobs.objects.filter(address='10 basejob road').first())
		time2 = strftime("%H:%M")

		new_scheduled_item = Scheduled_items.objects.filter('test schedule item super').first()
		new_audit_object =find_audit_object(new_scheduled_item, 'CREATE')

		self.assertEquals(new_audit_object.action, 'CREATE')
		self.assertEquals(new_audit_object.table, 'Item_Flow_scheduled_items')
		self.assertEquals(new_audit_object.pkey, new_scheduled_item.pk)
		self.assertEquals(new_audit_object.description, f'{new_scheduled_item.description} scheduled item created')
		self.assertEquals(new_audit_object.user, 'super')
		self.assertEquals(new_audit_object.date, settings.NOW)
		if time == time2:
			self.assertEquals(new_audit_object.time, time)
		else:
			self.assertEquals(new_audit_object.time, time2)

	def test_create_schedule_item_manager(self):
		self.loginManager()
		time = strftime("%H:%M")
		self.create_schedule_item(description='test schedule item manager', date_1=settings.NOW, quantity=1, job=Jobs.objects.filter(address='10 basejob road').first())
		time2 = strftime("%H:%M")

		new_scheduled_item = Scheduled_items.objects.filter('test schedule item manager').first()
		new_audit_object =find_audit_object(new_scheduled_item, 'CREATE')

		self.assertEquals(new_audit_object.action, 'CREATE')
		self.assertEquals(new_audit_object.table, 'Item_Flow_scheduled_items')
		self.assertEquals(new_audit_object.pkey, new_scheduled_item.pk)
		self.assertEquals(new_audit_object.description, f'{new_scheduled_item.description} scheduled item created') 
		self.assertEquals(new_audit_object.user, 'manager')
		self.assertEquals(new_audit_object.date, settings.NOW)
		if time == time2:
			self.assertEquals(new_audit_object.time, time)
		else:
			self.assertEquals(new_audit_object.time, time2)

	
	def test_create_purchase_order_super(self): # this also tests item creation (aside from acquired shopping list items)
		time = strftime("%H:%M")
		self.create_purchase_order(
			supplier_ref='po create super test',
			description1='po super desc 1', fullname1='po super fname 1', delivery_date1=settings.NOW, quantity1=1, price1=1, job1=Jobs.objects.filter(address='10 basejob road').first(), delivery_location1='shop',
			description2='po super desc 2', fullname2='po super fname 2', delivery_date2=settings.NOW, quantity2=1, price2=1, job2=Jobs.objects.filter(address='10 basejob road').first(), delivery_location2='shop'
			)
		time2 = strftime("%H:%M")


		new_purchase_order = Purchase_orders.objects.filter(supplier_ref='po create super test').first()
		new_purchase_order_audit_object = find_audit_object(new_purchase_order, 'CREATE')

		po_super_item_1 = Items.objects.filter(description='po super desc 1').first()
		po_super_item_1_audit_object = find_audit_object(po_super_item_1, 'CREATE')

		po_super_item_2 = Items.objects.filter(description='po super desc 2').first()
		po_super_item_2_audit_object = find_audit_object(po_super_item_2, 'CREATE')

		# assert PO audit
		self.assertEquals(new_purchase_order_audit_object.action, 'CREATE')
		self.assertEquals(new_purchase_order_audit_object.table, 'Item_Flow_purchase_orders')
		self.assertEquals(new_purchase_order_audit_object.pkey, new_purchase_order.pk)
		self.assertEquals(new_purchase_order_audit_object.description, f'purchase order no.{new_purchase_order} created')
		self.assertEquals(new_purchase_order_audit_object.user, 'super')
		if time == time2:
			self.assertEquals(new_audit_object.time, time)
		else:
			self.assertEquals(new_audit_object.time, time2)

		# assert item 1 audit
		self.assertEquals(po_super_item_1_audit_object.action, 'CREATE')
		self.assertEquals(po_super_item_1_audit_object.table, 'Item_Flow_items')
		self.assertEquals(po_super_item_1_audit_object.pkey, po_super_item_1.pk)
		self.assertEquals(po_super_item_1_audit_object.description, f'{po_super_item_1.fullname} created')
		self.assertEquals(po_super_item_1_audit_object.user, 'super')
		if time == time2:
			self.assertEquals( po_super_item_1_audit_object.time, time)
		else:
			self.assertEquals( po_super_item_1_audit_object.time, time2)

		# assert item 2 audit
		self.assertEquals(po_super_item_2_audit_object.action, 'CREATE')
		self.assertEquals(po_super_item_2_audit_object.table, 'Item_Flow_items')
		self.assertEquals(po_super_item_2_audit_object.pkey, po_super_item_2.pk)
		self.assertEquals(po_super_item_1_audit_object.description, f'{po_super_item_2.fullname} created')
		self.assertEquals(po_super_item_2_audit_object.user, 'super')
		if time == time2:
			self.assertEquals( po_super_item_2_audit_object.time, time)
		else:
			self.assertEquals( po_super_item_2_audit_object.time, time2)


	def test_create_purchase_order_manager(self): # this also tests item creation (aside from acquired shopping list items)
		self.loginManager()

		time = strftime("%H:%M")
		self.create_purchase_order(
			supplier_ref='po create manager test',
			description1='po manager desc 1', fullname1='po manager fname 1', delivery_date1=settings.NOW, quantity1=1, price1=1, job1=Jobs.objects.filter(address='10 basejob road').first(), delivery_location1='shop',
			description2='po manager desc 2', fullname2='po manager fname 2', delivery_date2=settings.NOW, quantity2=1, price2=1, job2=Jobs.objects.filter(address='10 basejob road').first(), delivery_location2='shop'
			)
		time2 = strftime("%H:%M")


		new_purchase_order = Purchase_orders.objects.filter(supplier_ref='po create manager test').first()
		new_purchase_order_audit_object = find_audit_object(new_purchase_order, 'CREATE')

		po_manager_item_1 = Items.objects.filter(description='po manager desc 1').first()
		po_manager_item_1_audit_object = find_audit_object(po_manager_item_1, 'CREATE')

		po_manager_item_2 = Items.objects.filter(description='po manager desc 2').first()
		po_manager_item_2_audit_object = find_audit_object(po_manager_item_2, 'CREATE')

		# assert PO audit
		self.assertEquals(new_purchase_order_audit_object.action, 'CREATE')
		self.assertEquals(new_purchase_order_audit_object.table, 'Item_Flow_purchase_orders')
		self.assertEquals(new_purchase_order_audit_object.pkey, new_purchase_order.pk)
		self.assertEquals(new_purchase_order_audit_object.description, f'purchase order no.{new_purchase_order} created')
		self.assertEquals(new_purchase_order_audit_object.user, 'manager')
		if time == time2:
			self.assertEquals(new_audit_object.time, time)
		else:
			self.assertEquals(new_audit_object.time, time2)

		# assert item 1 audit
		self.assertEquals(po_manager_item_1_audit_object.action, 'CREATE')
		self.assertEquals(po_manager_item_1_audit_object.table, 'Item_Flow_items')
		self.assertEquals(po_manager_item_1_audit_object.pkey, po_manager_item_1.pk)
		self.assertEquals(po_manager_item_1_audit_object.description, f'{po_manager_item_1.fullname} created')
		self.assertEquals(po_manager_item_1_audit_object.user, 'manager')
		if time == time2:
			self.assertEquals( po_manager_item_1_audit_object.time, time)
		else:
			self.assertEquals( po_manager_item_1_audit_object.time, time2)

		# assert item 2 audit
		self.assertEquals(po_manager_item_2_audit_object.action, 'CREATE')
		self.assertEquals(po_manager_item_2_audit_object.table, 'Item_Flow_items')
		self.assertEquals(po_manager_item_2_audit_object.pkey, po_manager_item_2.pk)
		self.assertEquals(po_manager_item_1_audit_object.description, f'{po_manager_item_2.fullname} created')
		self.assertEquals(po_manager_item_2_audit_object.user, 'manager')
		if time == time2:
			self.assertEquals( po_manager_item_2_audit_object.time, time)
		else:
			self.assertEquals( po_manager_item_2_audit_object.time, time2)


	def test_create_shopping_list_item_shopping_list_page_super(self):
		time = strftime("%H:%M")
		self.create_shopping_list_item(description='shopping list page super create', quantity=1, job=Jobs.objects.filter(address='10 basejob road').first())
		time2 = strftime("%H:%M")

		new_shopping_list_item = Shopping_list_items.objects.filter(description='shopping list page super create').first()
		new_shopping_list_item_audit_object = find_audit_object(new_shopping_list_item, 'CREATE')

		self.assertEquals(new_shopping_list_item_audit_object.action, 'CREATE')
		self.assertEquals(new_shopping_list_item_audit_object.table, 'Shopping_list_shopping_list_items')
		self.assertEquals(new_shopping_list_item_audit_object.pkey, new_shopping_list_item.pk)
		self.assertEquals(new_shopping_list_item_audit_object.user, 'super')
		if time == time2:
			self.assertEquals(new_shopping_list_item_audit_object.time, time)
		else:
			print('timestamp not tested')


	def test_create_shopping_list_item_shopping_list_page_manager(self):
		self.loginManager()
		time = strftime("%H:%M")
		self.create_shopping_list_item(description='shopping list page manager create', quantity=1, job=Jobs.objects.filter(address='10 basejob road').first())
		time2 = strftime("%H:%M")

		new_shopping_list_item = Shopping_list_items.objects.filter(description='shopping list page manager create').first()
		new_shopping_list_item_audit_object = find_audit_object(new_shopping_list_item, 'CREATE')

		self.assertEquals(new_shopping_list_item_audit_object.action, 'CREATE')
		self.assertEquals(new_shopping_list_item_audit_object.table, 'Shopping_list_shopping_list_items')
		self.assertEquals(new_shopping_list_item_audit_object.pkey, new_shopping_list_item.pk)
		self.assertEquals(new_shopping_list_item_audit_object.user, 'manager')
		if time == time2:
			self.assertEquals(new_shopping_list_item_audit_object.time, time)
		else:
			print('timestamp not tested')


	def test_create_shopping_list_item_shopping_list_page_staff(self):
		self.loginStaff()
		time = strftime("%H:%M")
		self.create_shopping_list_item(description='shopping list page staff create', quantity=1, job=Jobs.objects.filter(address='10 basejob road').first())
		time2 = strftime("%H:%M")

		new_shopping_list_item = Shopping_list_items.objects.filter(description='shopping list page staff create').first()
		new_shopping_list_item_audit_object = find_audit_object(new_shopping_list_item, 'CREATE')

		self.assertEquals(new_shopping_list_item_audit_object.action, 'CREATE')
		self.assertEquals(new_shopping_list_item_audit_object.table, 'Shopping_list_shopping_list_items')
		self.assertEquals(new_shopping_list_item_audit_object.pkey, new_shopping_list_item.pk)
		self.assertEquals(new_shopping_list_item_audit_object.user, 'staff')
		if time == time2:
			self.assertEquals(new_shopping_list_item_audit_object.time, time)
		else:
			print('timestamp not tested')


	def test_create_shopping_list_item_shopping_list_homepage_super(self):
		time = strftime("%H:%M")
		self.create_shopping_list_item(description='shopping list page homepage super create', quantity=1, job=Jobs.objects.filter(address='10 basejob road').first(), homepage=True)
		time2 = strftime("%H:%M")

		new_shopping_list_item = Shopping_list_items.objects.filter(description='shopping list page homepage super create').first()
		new_shopping_list_item_audit_object = find_audit_object(new_shopping_list_item, 'CREATE')

		self.assertEquals(new_shopping_list_item_audit_object.action, 'CREATE')
		self.assertEquals(new_shopping_list_item_audit_object.table, 'Shopping_list_shopping_list_items')
		self.assertEquals(new_shopping_list_item_audit_object.pkey, new_shopping_list_item.pk)
		self.assertEquals(new_shopping_list_item_audit_object.user, 'super')
		if time == time2:
			self.assertEquals(new_shopping_list_item_audit_object.time, time)
		else:
			print('timestamp not tested')


	def test_create_shopping_list_item_shopping_list_page_manager(self):
		self.loginManager()
		time = strftime("%H:%M")
		self.create_shopping_list_item(description='shopping list page homepage manager create', quantity=1, job=Jobs.objects.filter(address='10 basejob road').first(), homepage=True)
		time2 = strftime("%H:%M")

		new_shopping_list_item = Shopping_list_items.objects.filter(description='shopping list page homepage manager create').first()
		new_shopping_list_item_audit_object = find_audit_object(new_shopping_list_item, 'CREATE')

		self.assertEquals(new_shopping_list_item_audit_object.action, 'CREATE')
		self.assertEquals(new_shopping_list_item_audit_object.table, 'Shopping_list_shopping_list_items')
		self.assertEquals(new_shopping_list_item_audit_object.pkey, new_shopping_list_item.pk)
		self.assertEquals(new_shopping_list_item_audit_object.user, 'manager')
		if time == time2:
			self.assertEquals(new_shopping_list_item_audit_object.time, time)
		else:
			print('timestamp not tested')


	def test_create_shopping_list_item_shopping_list_page_staff(self):
		self.loginStaff()
		time = strftime("%H:%M")
		self.create_shopping_list_item(description='shopping list page homepage staff create', quantity=1, job=Jobs.objects.filter(address='10 basejob road').first(), homepage=True)
		time2 = strftime("%H:%M")

		new_shopping_list_item = Shopping_list_items.objects.filter(description='shopping list page homepage staff create').first()
		new_shopping_list_item_audit_object = find_audit_object(new_shopping_list_item, 'CREATE')

		self.assertEquals(new_shopping_list_item_audit_object.action, 'CREATE')
		self.assertEquals(new_shopping_list_item_audit_object.table, 'Shopping_list_shopping_list_items')
		self.assertEquals(new_shopping_list_item_audit_object.pkey, new_shopping_list_item.pk)
		self.assertEquals(new_shopping_list_item_audit_object.user, 'staff')
		if time == time2:
			self.assertEquals(new_shopping_list_item_audit_object.time, time)
		else:
			print('timestamp not tested')

	def test_create_admin_note_super(self):
		time = strftime("%H:%M")
		self.create_admin_note(title='create admin note super test', text='create admin note super test')
		time2 = strftime("%H:%M")

		new_admin_note = Notes.objects.filter(title='create admin note super test').first()
		new_admin_note_audit_object = find_audit_object(new_admin_note, 'CREATE')

		self.assertEquals(new_admin_note_audit_object.action, 'CREATE')
		self.assertEquals(new_admin_note_audit_object.table, 'Notes_notes')
		self.assertEquals(new_admin_note_audit_object.pkey, new_admin_note.pk)
		self.assertEquals(new_admin_note_audit_object.user, 'super')
		if time == time2:
			self.assertEquals(new_admin_note_audit_object.time, time)
		else:
			print('timestamp not tested')

	def test_create_admin_note_manager(self):
		time = strftime("%H:%M")
		self.create_admin_note(title='create admin note manager test', text='create admin note manager test')
		time2 = strftime("%H:%M")

		new_admin_note = Notes.objects.filter(title='create admin note manager test').first()
		new_admin_note_audit_object = find_audit_object(new_admin_note, 'CREATE')

		self.assertEquals(new_admin_note_audit_object.action, 'CREATE')
		self.assertEquals(new_admin_note_audit_object.table, 'Notes_notes')
		self.assertEquals(new_admin_note_audit_object.pkey, new_admin_note.pk)
		self.assertEquals(new_admin_note_audit_object.user, 'manager')
		if time == time2:
			self.assertEquals(new_admin_note_audit_object.time, time)
		else:
			print('timestamp not tested')


	def test_create_job_note_super(self):
		time = strftime("%H:%M")
		self.create_job_note(title='test create job note super', text='test create job note super', job=Jobs.objects.filter(address='10 basejob road').first())
		time2 = strftime("%H:%M")

		new_job_note = Notes.objects.filter(title='test create job note super').first()
		new_job_note_audit_object = find_audit_object(new_job_note, 'CREATE').first()

		self.assertEquals(new_job_note_audit_object.action, 'CREATE')
		self.assertEquals(new_job_note_audit_object.table, 'Notes_notes')
		self.assertEquals(new_job_note_audit_object.pkey, new_job_note.pk)
		self.assertEquals(new_job_note_audit_object.user, 'super')
		if time == time2:
			self.assertEquals(new_job_note_audit_object.time, time)
		else:
			print('timestamp not tested')


	def test_create_job_note_manager(self):
		time = strftime("%H:%M")
		self.create_job_note(title='test create job note manager', text='test create job note manager', job=Jobs.objects.filter(address='10 basejob road').first())
		time2 = strftime("%H:%M")

		new_job_note = Notes.objects.filter(title='test create job note manager').first()
		new_job_note_audit_object = find_audit_object(new_job_note, 'CREATE').first()

		self.assertEquals(new_job_note_audit_object.action, 'CREATE')
		self.assertEquals(new_job_note_audit_object.table, 'Notes_notes')
		self.assertEquals(new_job_note_audit_object.pkey, new_job_note.pk)
		self.assertEquals(new_job_note_audit_object.user, 'manager')
		if time == time2:
			self.assertEquals(new_job_note_audit_object.time, time)
		else:
			print('timestamp not tested')



#-- UPDATES --#

#- job -#

	def test_update_job_statuses_super(self):
		job = Jobs.objects.filter(address='10 basejob road').first()

		# super updates job to ongoing
		ongoing_time = strftime("%H:%M")
		self.update_job_status(job, 'ongoing')
		ongoing_time2 = strftime("%H:%M")

		job_ongoing_update_audit_object = find_audit_object(job, 'STATUS CHANGE -> ONGOING')

		self.assertEquals(job_ongoing_update_audit_object.action, 'STATUS CHANGE -> ONGOING')
		self.assertEquals(job_ongoing_update_audit_object.table, 'Jobs_jobs')
		self.assertEquals(job_ongoing_update_audit_object.pkey, job.pk)
		self.assertEquals(job_ongoing_update_audit_object.description, '10 basejob road')
		self.assertEquals(job_ongoing_update_audit_object.user, 'super')
		if ongoing_time == ongoing_time2:
			self.assertEquals(job_ongoing_update_audit_object.time, ongoing_time)
		else:
			print('timestamp not tested')

		# super updates job to completed
		completed_time = strftime("%H:%M")
		self.update_job_status(job, 'completed')
		completed_time2 = strftime("%H:%M")

		job_completed_update_audit_object = find_audit_object(job, 'STATUS CHANGE -> COMPLETED')

		self.assertEquals(job_ongoing_update_audit_object.action, 'STATUS CHANGE -> COMPLETED')
		self.assertEquals(job_ongoing_update_audit_object.table, 'Jobs_jobs')
		self.assertEquals(job_ongoing_update_audit_object.pkey, job.pk)
		self.assertEquals(job_ongoing_update_audit_object.description, '10 basejob road')
		self.assertEquals(job_ongoing_update_audit_object.user, 'super')
		if completed_time == completed_time2:
			self.assertEquals(job_ongoing_update_audit_object.time, completed_time)
		else:
			print('timestamp not tested')

		# super updates job to quote
		quote_time = strftime("%H:%M")
		self.update_job_status(job, 'quote')
		quote_time2 = strftime("%H:%M")

		job_quote_update_audit_object = find_audit_object(job, 'STATUS CHANGE -> QUOTE')

		self.assertEquals(job_ongoing_update_audit_object.action, 'STATUS CHANGE -> QUOTE')
		self.assertEquals(job_ongoing_update_audit_object.table, 'Jobs_jobs')
		self.assertEquals(job_ongoing_update_audit_object.pkey, job.pk)
		self.assertEquals(job_ongoing_update_audit_object.description, '10 basejob road')
		self.assertEquals(job_ongoing_update_audit_object.user, 'super')
		if quote_time == quote_time2:
			self.assertEquals(job_ongoing_update_audit_object.time, quote_time)
		else:
			print('timestamp not tested')


	def test_update_job_status_manager(self):
		self.loginManager()
		job = Jobs.objects.filter(address='10 basejob road').first()

		# manager updates job to ongoing
		ongoing_time = strftime("%H:%M")
		self.update_job_status(job, 'ongoing')
		ongoing_time2 = strftime("%H:%M")

		job_ongoing_update_audit_object = find_audit_object(job, 'STATUS CHANGE -> ONGOING')

		self.assertEquals(job_ongoing_update_audit_object.action, 'STATUS CHANGE -> ONGOING')
		self.assertEquals(job_ongoing_update_audit_object.table, 'Jobs_jobs')
		self.assertEquals(job_ongoing_update_audit_object.pkey, job.pk)
		self.assertEquals(job_ongoing_update_audit_object.description, '10 basejob road')
		self.assertEquals(job_ongoing_update_audit_object.user, 'manager')
		if ongoing_time == ongoing_time2:
			self.assertEquals(job_ongoing_update_audit_object.time, ongoing_time)
		else:
			print('timestamp not tested')

		# manager updates job to completed
		completed_time = strftime("%H:%M")
		self.update_job_status(job, 'completed')
		completed_time2 = strftime("%H:%M")

		job_completed_update_audit_object = find_audit_object(job, 'STATUS CHANGE -> COMPLETED')

		self.assertEquals(job_ongoing_update_audit_object.action, 'STATUS CHANGE -> COMPLETED')
		self.assertEquals(job_ongoing_update_audit_object.table, 'Jobs_jobs')
		self.assertEquals(job_ongoing_update_audit_object.pkey, job.pk)
		self.assertEquals(job_ongoing_update_audit_object.description, '10 basejob road')
		self.assertEquals(job_ongoing_update_audit_object.user, 'manager')
		if completed_time == completed_time2:
			self.assertEquals(job_ongoing_update_audit_object.time, completed_time)
		else:
			print('timestamp not tested')

		# manager updates job to quote
		quote_time = strftime("%H:%M")
		self.update_job_status(job, 'quote')
		quote_time2 = strftime("%H:%M")

		job_quote_update_audit_object = find_audit_object(job, 'STATUS CHANGE -> QUOTE')

		self.assertEquals(job_ongoing_update_audit_object.action, 'STATUS CHANGE -> QUOTE')
		self.assertEquals(job_ongoing_update_audit_object.table, 'Jobs_jobs')
		self.assertEquals(job_ongoing_update_audit_object.pkey, job.pk)
		self.assertEquals(job_ongoing_update_audit_object.description, '10 basejob road')
		self.assertEquals(job_ongoing_update_audit_object.user, 'manager')
		if quote_time == quote_time2:
			self.assertEquals(job_ongoing_update_audit_object.time, quote_time)
		else:
			print('timestamp not tested')


#- schedule_item -#

	def test_update_schedule_item_dates_super(self):
		today = date.today()
		tomorrow = today + relativdelta(days=1)
		new_date_1 = tomorrow + relativdelta(days=1)
		new_date_2 = new_date_1 + relativdelta(days=1)
		job = Jobs.objects.filter(address='10 basejob road').first()
		self.create_schedule_item(description='test update schedule item dates super', date_1=today, date_2=tomorrow, quantity=1, job=job)
		schedule_item = Scheduled_items.objects.filter(description='test update schedule item dates super').first()

		time = strftime("%H:%M")
		self.update_schedule_item_date(schedule_item, new_date_1, new_date_2)
		time2 = strftime("%H:%M")


		schedule_item_date_update_audit_object = find_audit_object(schedule_item, f'DATE UPDATE: {today}, {tomorrow} -> {new_date_1}, {new_date_2}')

		self.assertEquals(schedule_item_date_update_audit_object.action, f'DATE UPDATE: {today}, {tomorrow} -> {new_date_1}, {new_date_2}')
		self.assertEquals(schedule_item_date_update_audit_object.table, 'Item_Flow_scheduled_items')
		self.assertEquals(schedule_item_date_update_audit_object.pkey, Schedule_item.pk)
		self.assertEquals(schedule_item_date_update_audit_object.description, schedule_item.description)
		self.assertEquals(schedule_item_date_update_audit_object.user, 'super')
		if time == time2:
			self.assertEquals(schedule_item_date_update_audit_object.time, time)#
		else:
			print('timestamp not tested')

	def test_update_schedule_item_dates_manager(self):
		today = date.today()
		tomorrow = today + relativdelta(days=1)
		new_date_1 = tomorrow + relativdelta(days=1)
		new_date_2 = new_date_1 + relativdelta(days=1)
		job = Jobs.objects.filter(address='10 basejob road').first()
		self.create_schedule_item(description='test update schedule item dates manager', date_1=today, date_2=tomorrow, quantity=1, job=job)
		schedule_item = Scheduled_items.objects.filter(description='test update schedule item dates manager').first()

		time = strftime("%H:%M")
		self.update_schedule_item_date(schedule_item, new_date_1, new_date_2)
		time2 = strftime("%H:%M")


		schedule_item_date_update_audit_object = find_audit_object(schedule_item, f'DATE UPDATE: {today}, {tomorrow} -> {new_date_1}, {new_date_2}')

		self.assertEquals(schedule_item_date_update_audit_object.action, f'DATE UPDATE: {today}, {tomorrow} -> {new_date_1}, {new_date_2}')
		self.assertEquals(schedule_item_date_update_audit_object.table, 'Item_Flow_scheduled_items')
		self.assertEquals(schedule_item_date_update_audit_object.pkey, Schedule_item.pk)
		self.assertEquals(schedule_item_date_update_audit_object.description, schedule_item.description)
		self.assertEquals(schedule_item_date_update_audit_object.user, 'manager')
		if time == time2:
			self.assertEquals(schedule_item_date_update_audit_object.time, time)
		else:
			print('timestamp not tested')


#- purchase order -#

	def test_update_purchase_order_supplier_ref_super(self):
		self.create_purchase_order(
			supplier_ref='test update purchase order supplier ref super',
			description1='po supplier ref update desc 1', fullname1='po supplier ref update fname 1', delivery_date1=settings.NOW, quantity1=1, price1=1, job1=Jobs.objects.filter(address='10 basejob road').first(), delivery_location1='shop',
			description2='po supplier ref update desc 2', fullname2='po supplier ref update fname 2', delivery_date2=settings.NOW, quantity2=1, price2=1, job2=Jobs.objects.filter(address='10 basejob road').first(), delivery_location2='shop'
			)
		PO = Purchase_orders.objects.filter(supplier_ref='test update purchase order supplier ref super').first()

		time = strftime("%H:%M")
		self.update_PO_supplier_ref(purchase_order=PO, new_ref='updated ref')
		time2 = strftime("%H:%M")

		update_PO_supplier_ref_audit_object = find_audit_object(PO, f'UPDATE SUPPLIER REF: "test update purchase order supplier ref super" -> "updated ref"')

		self.assertEquals(update_PO_supplier_ref_audit_object.action, f'UPDATE SUPPLIER REF: "test update purchase order supplier ref super" -> "updated ref"')
		self.assertEquals(update_PO_supplier_ref_audit_object.table, 'Item_Flow_purchase_orders')
		self.assertEquals(update_PO_supplier_ref_audit_object.pkey, PO.id)
		self.assertEquals(update_PO_supplier_ref_audit_object.description, f'order no.: {PO.id+4000}')
		self.assertEquals(update_PO_supplier_ref_audit_object.user, 'super')
		if time == time2:
			self.assertEquals(update_PO_supplier_ref_audit_object.time, time)
		else:
			print('timestamp not tested')


#- Item -#

	def test_mark_showroom_super(self):
		self.create_purchase_order(
			self, Supplier_ref='test_mark_showroom_super',
			description1='test mark showroom super 1 desc', fullname1='test mark showroom super 1 fname', delivery_date1=settings.NOW, quantity1=1, price1=1, job1=Jobs.objects.filter('10 basejob road').first(), delivery_location1='shop'
			)
		item = Items.objects.filter(description='test mark showroom super 1 desc').first()

		time = strftime("%H:%M")
		self.mark_showroom(item)
		time2 = strftime("%H:%M")

		item_marked_showroom_audit_object = find_audit_object(item, 'MARK SHOWROOM')

		self.assertEquals(item_marked_showroom_audit_object.action, 'MARK SHOWROOM')
		self.assertEquals(item_marked_showroom_audit_object.table, 'Item_Flow_items')
		self.assertEquals(item_marked_showroom_audit_object.pkey, item.pk)
		self.assertEquals(item_marked_showroom_audit_object.description, f'{item.fullname}. Order no.:{item.PO}')
		self.assertEquals(item_marked_showroom_audit_object.user, 'super')
		self.assertEquals(item_marked_showroom_audit_object.date, settings.NOW)
		if time == time2:
			self.assertEquals(item_marked_showroom_audit_object.time, time)
		else:
			print('timestamp not tested')


	def test_mark_showroom_manager(self):
		self.create_purchase_order(
			self, Supplier_ref='test_mark_showroom_manager',
			description1='test mark showroom manager 1 desc', fullname1='test mark showroom manager 1 fname', delivery_date1=settings.NOW, quantity1=1, price1=1, job1=Jobs.objects.filter('10 basejob road').first(), delivery_location1='shop'
			)
		item = Items.objects.filter(description='test mark showroom manager 1 desc').first()

		time = strftime("%H:%M")
		self.mark_showroom(item)
		time2 = strftime("%H:%M")

		item_marked_showroom_audit_object = find_audit_object(item, 'MARK SHOWROOM')

		self.assertEquals(item_marked_showroom_audit_object.action, 'MARK SHOWROOM')
		self.assertEquals(item_marked_showroom_audit_object.table, 'Item_Flow_items')
		self.assertEquals(item_marked_showroom_audit_object.pkey, item.pk)
		self.assertEquals(item_marked_showroom_audit_object.description, f'{item.fullname}. Order no.:{item.PO}')
		self.assertEquals(item_marked_showroom_audit_object.user, 'manager')
		self.assertEquals(item_marked_showroom_audit_object.date, settings.NOW)
		if time == time2:
			self.assertEquals(item_marked_showroom_audit_object.time, time)
		else:
			print('timestamp not tested')

	def test_mark_on_site_super(self):
		self.create_purchase_order(
			self, Supplier_ref='test_mark_on_site_super',
			description1='test mark on site super 1 desc', fullname1='test mark on site super 1 fname', delivery_date1=settings.NOW, quantity1=1, price1=1, job1=Jobs.objects.filter('10 basejob road').first(), delivery_location1='shop'
			)
		item = Items.objects.filter(description='test mark on site super 1 desc').first()

		time = strftime("%H:%M")
		self.mark_on_site(item)
		time2 = strftime("%H:%M")

		item_marked_showroom_audit_object = find_audit_object(item, 'MARK ON SITE')

		self.assertEquals(item_marked_showroom_audit_object.action, 'MARK ON SITE')
		self.assertEquals(item_marked_showroom_audit_object.table, 'Item_Flow_items')
		self.assertEquals(item_marked_showroom_audit_object.pkey, item.pk)
		self.assertEquals(item_marked_showroom_audit_object.description, f'{item.fullname}. Order no.:{item.PO}')
		self.assertEquals(item_marked_showroom_audit_object.user, 'super')
		self.assertEquals(item_marked_showroom_audit_object.date, settings.NOW)
		if time == time2:
			self.assertEquals(item_marked_showroom_audit_object.time, time)
		else:
			print('timestamp not tested')


	def test_mark_on_site_manager(self):
		self.create_purchase_order(
			self, Supplier_ref='test_mark_on_site_manager',
			description1='test mark on site manager 1 desc', fullname1='test mark on site manager 1 fname', delivery_date1=settings.NOW, quantity1=1, price1=1, job1=Jobs.objects.filter('10 basejob road').first(), delivery_location1='shop'
			)
		item = Items.objects.filter(description='test mark on site manager 1 desc').first()

		time = strftime("%H:%M")
		self.mark_on_site(item)
		time2 = strftime("%H:%M")

		item_marked_showroom_audit_object = find_audit_object(item, 'MARK ON SITE')

		self.assertEquals(item_marked_showroom_audit_object.action, 'MARK ON SITE')
		self.assertEquals(item_marked_showroom_audit_object.table, 'Item_Flow_items')
		self.assertEquals(item_marked_showroom_audit_object.pkey, item.pk)
		self.assertEquals(item_marked_showroom_audit_object.description, f'{item.fullname}. Order no.:{item.PO}')
		self.assertEquals(item_marked_showroom_audit_object.user, 'manager')
		self.assertEquals(item_marked_showroom_audit_object.date, settings.NOW)
		if time == time2:
			self.assertEquals(item_marked_showroom_audit_object.time, time)
		else:
			print('timestamp not tested')


	def test_reject_and_reschedule_super(self):
		self.create_purchase_order_item(description='reject and reschedule super desc', fullname='reject and reschedule super fname', delivery_date=settings.NOW)
		item = Items.objects.filter(description='reject and reschedule super desc').first()

		time = strftime("%H:%M")
		self.reject_and_reschedule(item)
		time2 = strftime("%H:%M")
		item = Items.objects.filter(description='reject and reschedule super desc').first()

		reject_and_reschedule_item_audit_object = find_audit_object(item, f'UPDATE - rejected and rescheduled for {item.delivery_date}')

		self.assertEquals(reject_and_reschedule_item_audit_object.action, f'UPDATE - rejected and rescheduled for {item.delivery_date}')
		self.assertEquals(reject_and_reschedule_item_audit_object.table, 'Item_Flow_items')
		self.assertEquals(reject_and_reschedule_item_audit_object.pkey, item.pk)
		self.assertEquals(reject_and_reschedule_item_audit_object.description, f'{item.fullname}. Order no.:{item.PO}')
		self.assertEquals(reject_and_reschedule_item_audit_object.user, 'super')
		self.assertEquals(reject_and_reschedule_item_audit_object.date, settings.NOW)
		if time == time2:
			self.assertEquals(reject_and_reschedule_item_audit_object.time, time)
		else:
			print('timestamp not tested')


	def test_reject_and_reschedule_manager(self):
		self.loginManager()
		self.create_purchase_order_item(description='reject and reschedule manager desc', fullname='reject and reschedule manager fname', delivery_date=settings.NOW)
		item = Items.objects.filter(description='reject and reschedule manager desc').first()

		time = strftime("%H:%M")
		self.reject_and_reschedule(item)
		time2 = strftime("%H:%M")
		item = Items.objects.filter(description='reject and reschedule manager desc').first()

		reject_and_reschedule_item_audit_object = find_audit_object(item, f'UPDATE - rejected and rescheduled for {item.delivery_date}')

		self.assertEquals(reject_and_reschedule_item_audit_object.action, f'UPDATE - rejected and rescheduled for {item.delivery_date}')
		self.assertEquals(reject_and_reschedule_item_audit_object.table, 'Item_Flow_items')
		self.assertEquals(reject_and_reschedule_item_audit_object.pkey, item.pk)
		self.assertEquals(reject_and_reschedule_item_audit_object.description, f'{item.fullname}. Order no.:{item.PO}')
		self.assertEquals(reject_and_reschedule_item_audit_object.user, 'manager')
		self.assertEquals(reject_and_reschedule_item_audit_object.date, settings.NOW)
		if time == time2:
			self.assertEquals(reject_and_reschedule_item_audit_object.time, time)
		else:
			print('timestamp not tested')


	def test_reject_and_cancel_super(self):
		self.create_purchase_order_item(description='reject and cancel super desc', fullname='reject and cancel super fname', delivery_date=settings.NOW)
		item = Items.objects.filter(description='reject and cancel super desc').first()

		time = strftime("%H:%M")
		self.reject_and_cancel(item)
		time2 = strftime("%H:%M")

		reject_and_cancel_item_audit_object = find_audit_object(item, 'DELETE - rejected and cancelled')

		self.assertEquals(reject_and_cancel_item_audit_object.action, 'DELETE - rejected and cancelled')
		self.assertEquals(reject_and_cancel_item_audit_object.table, 'Item_Flow_items')
		self.assertEquals(reject_and_cancel_item_audit_object.pkey, item.pk)
		self.assertEquals(reject_and_cancel_item_audit_object.description, f'{item.fullname}. Order no.:{item.PO}')
		self.assertEquals(reject_and_cancel_item_audit_object.user, 'super')
		self.assertEquals(reject_and_cancel_item_audit_object.date, settings.NOW)
		if time == time2:
			self.assertEquals(reject_and_cancel_item_audit_object.time, time)
		else:
			print('timestamp not tested')


	def test_reject_and_cancel_manager(self):
		self.create_purchase_order_item(description='reject and cancel manager desc', fullname='reject and cancel manager fname', delivery_date=settings.NOW)
		item = Items.objects.filter(description='reject and cancel manager desc').first()

		time = strftime("%H:%M")
		self.reject_and_cancel(item)
		time2 = strftime("%H:%M")

		reject_and_cancel_item_audit_object = find_audit_object(item, 'DELETE - rejected and cancelled')

		self.assertEquals(reject_and_cancel_item_audit_object.action, 'DELETE - rejected and cancelled')
		self.assertEquals(reject_and_cancel_item_audit_object.table, 'Item_Flow_items')
		self.assertEquals(reject_and_cancel_item_audit_object.pkey, item.pk)
		self.assertEquals(reject_and_cancel_item_audit_object.description, f'{item.fullname}. Order no.:{item.PO}')
		self.assertEquals(reject_and_cancel_item_audit_object.user, 'manager')
		self.assertEquals(reject_and_cancel_item_audit_object.date, settings.NOW)
		if time == time2:
			self.assertEquals(reject_and_cancel_item_audit_object.time, time)
		else:
			print('timestamp not tested')



#- shopping list -#

	def test_super_acquires_shopping_list_item(self):
		# remember that when an sli is acquired it is deleted and replaced with an Item_Flow_items object
		self.create_shopping_list_item(description='super acquires shopping list item', quantity=1, job=Jobs.objects.first())
		sli = Shopping_list_items.objects.filter(description='super acquires shopping list item').first()

		time = strftime("%H:%M")
		self.mark_shopping_list_item_acquired(sli)
		time2 = strftime("%H:%M")
		acquired_item = Items.objects.get(description='super acquires shopping list item').first()

		sli_acquired_audit_object = find_audit_object(sli, f'ACQUIRED - {sli.description} acquired')

		self.assertEquals(sli_acquired_audit_object.action, f'ACQUIRED - {sli.description} acquired')
		self.assertEquals(sli_acquired_audit_object.table, 'Shopping_list_shopping_list_items')
		self.assertEquals(sli_acquired_audit_object.pkey, sli.pk)
		self.assertEquals(sli_acquired_audit_object.description, f'{sli.descrtiption} marked as acquired, new object: Item_Flow_items - pk={acquired_item.pk}')
		self.assertEquals(sli_acquired_audit_object.user, 'super')
		self.assertEquals(sli_acquired_audit_object.date, settings.NOW)
		if time == time2:
			self.assertEquals(sli_acquired_audit_object.time, time)
		else:
			print('timestamp not tested')


	def test_manager_acquires_shopping_list_item(self):
		self.loginManager()
		# remember that when an sli is acquired it is deleted and replaced with an Item_Flow_items object
		self.create_shopping_list_item(description='manager acquires shopping list item', quantity=1, job=Jobs.objects.first())
		sli = Shopping_list_items.objects.filter(description='manager acquires shopping list item').first()

		time = strftime("%H:%M")
		self.mark_shopping_list_item_acquired(sli)
		time2 = strftime("%H:%M")
		acquired_item = Items.objects.get(description='manager acquires shopping list item').first()

		sli_acquired_audit_object = find_audit_object(sli, f'ACQUIRED - {sli.description} acquired')

		self.assertEquals(sli_acquired_audit_object.action, f'ACQUIRED - {sli.description} acquired')
		self.assertEquals(sli_acquired_audit_object.table, 'Shopping_list_shopping_list_items')
		self.assertEquals(sli_acquired_audit_object.pkey, sli.pk)
		self.assertEquals(sli_acquired_audit_object.description, f'{sli.descrtiption} marked as acquired, new object: Item_Flow_items - pk={acquired_item.pk}')
		self.assertEquals(sli_acquired_audit_object.user, 'manager')
		self.assertEquals(sli_acquired_audit_object.date, settings.NOW)
		if time == time2:
			self.assertEquals(sli_acquired_audit_object.time, time)
		else:
			print('timestamp not tested')



#-- DELETES --#

	def test_job_delete_super(self):
		job = Jobs.objects.first()
		time = strftime("%H:%M")
		self.delete_job(job)
		time2 = strftime("%H:%M")

		job_delete_audit_object = find_audit_object(job, 'DELETED - job profile deleted')

		self.assertEquals(job_delete_audit_object.action, 'DELETED - job profile deleted')
		self.assertEquals(job_delete_audit_object.table, 'Jobs_jobs')
		self.assertEquals(job_delete_audit_object.pkey, job.pk)
		self.assertEquals(job_delete_audit_object.description, f'{job.address} profile deleted, along with all attached notes, items and other data')
		self.assertEquals(job_delete_audit_object.user, 'super')
		self.assertEquals(job_delete_audit_object.date, settings.NOW)
		if time == time2:
			self.assertEquals(job_delete_audit_object.time, time)
		else:
			print('timestamp not tested')


	def test_schedule_item_delete_super(self):
		self.create_schedule_item(description='test schedule item delete super', date_1=settings.NOW, job=Jobs.objects.first(), quantity=1)
		schedule_item = Scheduled_items.objects.filter(description='test schedule item delete super').first()
		time = strftime("%H:%M")
		self.delete_schedule_item(schedule_item)
		time2 = strftime("%H:%M")

		schedule_item_delete_audit_object = find_audit_object(schedule_item, 'DELETED')

		self.assertEquals(schedule_item_delete_audit_object.action, 'DELETED')
		self.assertEquals(schedule_item_delete_audit_object.table, 'Item_Flow_scheduled_items')
		self.assertEquals(schedule_item_delete_audit_object.pkey, schedule_item.pk)
		self.assertEquals(schedule_item_delete_audit_object.description, f'{schedule_item.description}')
		self.assertEquals(schedule_item_delete_audit_object.user, 'super')
		self.assertEquals(schedule_item_delete_audit_object.date, settings.NOW)
		if time == time2:
			self.assertEquals(schedule_item_delete_audit_object.time, time)
		else:
			print('timestamp not tested')

	
	def test_shopping_list_item_delete_super(self):
		self.create_shopping_list_item(description='test shopping list item delete super', job=Jobs.objects.first(), quantity=1)
		sli = Shopping_list_items.objects.filter(description='test shopping list item delete super').first()
		time = strftime("%H:%M")
		self.delete_shopping_list_item(sli=sli)
		time2 = strftime("%H:%M")

		shopping_list_item_delete_audit_object = find_audit_object(sli, 'DELETED')

		self.assertEquals(shopping_list_item_delete_audit_object.action, 'DELETED')
		self.assertEquals(shopping_list_item_delete_audit_object.table, 'Shopping_list_shopping_list_items')
		self.assertEquals(shopping_list_item_delete_audit_object.pkey, sli.pk)
		self.assertEquals(shopping_list_item_delete_audit_object.description, f'{sli.description} deleted')
		self.assertEquals(shopping_list_item_delete_audit_object.user, 'super')
		self.assertEquals(shopping_list_item_delete_audit_object.date, settings.NOW)
		if time == time2:
			self.assertEquals(shopping_list_item_delete_audit_object.time, time)
		else:
			print('timestamp not tested')

	
	def test_acquired_item_delete_super(self):
		self.create_acquired_shopping_list_item(description='test acquired item delete super', job=Jobs.objects.first(), quantity=1)
		asli = Items.objects.filter(description='test acquired item delete super').first()
		time = strftime("%H:%M")
		self.delete_acquired_shopping_list_item(asli)
		time2 = strftime("%H:%M")

		acquired_shopping_list_item_delete_audit_object = find_audit_object(asli, 'DELETED')

		self.assertEquals(acquired_shopping_list_item_delete_audit_object.action, 'DELETED')
		self.assertEquals(acquired_shopping_list_item_delete_audit_object.table, 'Item_Flow_items')
		self.assertEquals(acquired_shopping_list_item_delete_audit_object.pkey, asli.pk)
		self.assertEquals(acquired_shopping_list_item_delete_audit_object.description, f'{asli.description} deleted')
		self.assertEquals(acquired_shopping_list_item_delete_audit_object.user, 'super')
		self.assertEquals(acquired_shopping_list_item_delete_audit_object.date, settings.NOW)
		if time == time2:
			self.assertEquals(acquired_shopping_list_item_delete_audit_object.time, time)
		else:
			print('timestamp not tested')

	
	def test_item_delete_super(self):
		self.create_purchase_order_item(description='test delete item super desc', fullname='test delete item super fname', delivery_date=settings.NOW)
		item = Items.objects.filter(description='test delete item super desc').first()
		time = strftime("%H:%M")
		self.delete_item(item)
		time2 = strftime("%H:%M")

		item_delete_audit_object = find_audit_object(item, 'DELETED')

		self.assertEquals(item_delete_audit_object.action, 'DELETED')
		self.assertEquals(item_delete_audit_object.table, 'Item_Flow_items')
		self.assertEquals(item_delete_audit_object.pkey, item.pk)
		self.assertEquals(item_delete_audit_object.description, f'{item.fullname} deleted')
		self.assertEquals(item_delete_audit_object.user, 'super')
		self.assertEquals(item_delete_audit_object.date, settings.NOW)
		if time == time2:
			self.assertEquals(item_delete_audit_object.time, time)
		else:
			print('timestamp not tested')


	def test_note_delete_super(self):
		self.create_job_note(title='test note delete super title', text='test note delete super text', job=Jobs.objects.first())
		note = Notes.objects.filter(title='test note delete super title').first()
		time = strftime("%H:%M")
		self.delete_note(note)
		time2 = strftime("%H:%M")

		note_delete_audit_object = find_audit_object(note, 'DELETED')

		self.assertEquals(note_delete_audit_object.action, 'DELETED')
		self.assertEquals(note_delete_audit_object.table, 'Notes_notes')
		self.assertEquals(note_delete_audit_object.pkey, note.pk)
		self.assertEquals(note_delete_audit_object.description, f'title: {note.title} | text: {note.text}')
		self.assertEquals(note_delete_audit_object.user, 'super')
		self.assertEquals(note_delete_audit_object.date, settings.NOW)
		if time == time2:
			self.assertEquals(note_delete_audit_object.time, time)
		else:
			print('timestamp not tested')


# Jobs.objects.first()._meta.db_table <- displaying table name