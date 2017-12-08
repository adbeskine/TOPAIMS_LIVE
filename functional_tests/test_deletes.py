from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from home.models import Site_info, Jobs, Notes, Scheduled_items, Purchase_orders, Items, Shopping_list_items
from django.urls import reverse
from selenium.webdriver.support.ui import Select
from django.conf import settings
from dateutil.relativedelta import relativedelta
from datetime import date

class DeletesTest(FunctionalTest):

	# this test finds every single item that needs to be able to be deleted and tests the process to delete it
	# REFRACT - except scheduled items, the deletion test for that is in the schedule of items test

	#-- HELPER METHODS --#

	def click(self, element, base_element=None):
		if base_element:
			return ActionChains(self.browser).click(self.browser.find_element_by_id(base_element).find_element_by_id(element)).perform()
		else:
			return ActionChains(self.browser).click(self.browser.find_element_by_id(element)).perform()
	
	def wait_until_visible(self, element, base_element=None):
		if base_element:
			return self.wait_for(lambda: self.assertTrue(self.browser.find_element_by_id(base_element).find_element_by_id(element).is_displayed()))
		else:
			return self.wait_for(lambda: self.assertTrue(self.browser.find_element_by_id(element).is_displayed()))

	def create_custom_job(self, name, email, phone, address, note): # REFRACT make this actually create db objects instead of manually typing everything
		self.browser.get(self.live_server_url + reverse('new_job_form'))
		self.browser.find_element_by_id('Name').send_keys(name)
		self.browser.find_element_by_id('Email').send_keys(email)
		self.browser.find_element_by_id('Phone').send_keys(phone)
		self.browser.find_element_by_id('Address').send_keys(address)
		self.browser.find_element_by_id('Note').send_keys(note)
		ActionChains(self.browser).click(self.browser.find_element_by_id('create')).perform()
		self.wait_for(lambda: self.assertEqual(self.browser.title, f'TopMarks - {address}'))

	def add_job_note(self, title, text, job):
		self.browser.get(self.live_server_url+reverse('job', kwargs={'job_id':job.job_id}))
		self.browser.find_element_by_id('Title_input').send_keys(title)
		self.browser.find_element_by_id('Note_input').send_keys(text)
		ActionChains(self.browser).click(self.browser.find_element_by_id('Add_note')).perform()
		new_note = Notes.objects.filter(Title=title).first()
		self.wait_until_visible(f'Note_{new_note.pk}')

	def add_admin_note(self, title, text):
		self.browser.get(self.live_server_url+reverse('homepage'))
		self.browser.find_element_by_id('Title_input').send_keys(title)
		self.browser.find_element_by_id('Note_input').send_keys(text)
		ActionChains(self.browser).click(self.browser.find_element_by_id('Add_note')).perform()

	def add_shopping_list_item(self, description, quantity, job):
		self.browser.get(self.live_server_url + reverse('shopping_list'))
		self.browser.find_element_by_id('shopping_list_description_input').send_keys(description)
		self.browser.find_element_by_id('shopping_list_quantity_input').send_keys(quantity)
		job_input = Select(self.browser.find_element_by_id('shopping_list_job_input'))
		job_input.select_by_value(str(job.address))
		self.click('shopping_list_form_submit_button')

		new_shopping_list_item = Shopping_list_items.objects.filter(description=description).first()
		self.wait_until_visible(f'Shopping_list_items_{new_shopping_list_item.pk}')

	def add_acquired_shopping_list_item(self, description, quantity, job):
		self.add_shopping_list_item(description, quantity, job)
		new_shopping_list_item = Shopping_list_items.objects.filter(description=description).first()
		self.click(f'Shopping_list_items_{new_shopping_list_item.pk}_acquired_button')

		self.wait_for(lambda: self.assertIn(f'{new_shopping_list_item.description} acquired', self.browser.page_source))

	def create_purchase_order(
		self, 
		description, fullname, delivery_date, job, supplier='Stark Industries', supplier_ref='123', quantity=1, price=10, delivery_location='shop',
		description2=None, fullname2=None, delivery_date2=None, job2=None, quantity2=None, price2=None, delivery_location2=None,
		description3=None, fullname3=None, delivery_date3=None, job3=None, quantity3=None, price3=None, delivery_location3=None,
		description4=None, fullname4=None, delivery_date4=None, job4=None, quantity4=None, price4=None, delivery_location4=None,
		description5=None, fullname5=None, delivery_date5=None, job5=None, quantity5=None, price5=None, delivery_location5=None,
		description6=None, fullname6=None, delivery_date6=None, job6=None, quantity6=None, price6=None, delivery_location6=None,
		description7=None, fullname7=None, delivery_date7=None, job7=None, quantity7=None, price7=None, delivery_location7=None,
		description8=None, fullname8=None, delivery_date8=None, job8=None, quantity8=None, price8=None, delivery_location8=None,
		description9=None, fullname9=None, delivery_date9=None, job9=None, quantity9=None, price9=None, delivery_location9=None,
		description10=None, fullname10=None, delivery_date10=None, job10=None, quantity10=None, price10=None, delivery_location10=None
		):
		self.browser.get(self.live_server_url+reverse('job', kwargs={'job_id':job.job_id}))
		self.wait_for(lambda: self.browser.find_element_by_id('site_management_panel'))
		self.click('PO_panel_toggle')
		self.wait_for(lambda: self.assertTrue(self.browser.find_element_by_id('PO_panel').is_displayed()))
		self.assertTrue(self.browser.find_element_by_id('blank_PO_form').is_displayed())
		form = self.browser.find_element_by_id('blank_PO_form')

		form.find_element_by_id('supplier_input').send_keys(supplier)
		form.find_element_by_id('supplier_ref_input').send_keys(supplier_ref)


		form.find_element_by_id('item_1_description_input').send_keys(description)
		form.find_element_by_id('item_1_fullname_input').send_keys(fullname)
		form.find_element_by_id('item_1_price_input').send_keys(price)
		form_job = Select(form.find_element_by_id('item_1_job_input'))
		form_job.select_by_value(job.address)
		form_delivery_location = Select(form.find_element_by_id('item_1_delivery_location_input'))
		form_delivery_location.select_by_value(delivery_location)
		form.find_element_by_id('item_1_quantity_input').send_keys(quantity)

		delivery_date_day=Select(form.find_element_by_id('id_item_1_delivery_date_day'))
		delivery_date_day.select_by_value(str(delivery_date.day))

		delivery_date_year=Select(form.find_element_by_id('id_item_1_delivery_date_year'))
		delivery_date_year.select_by_value(str(delivery_date.year))

		delivery_date_month=Select(form.find_element_by_id('id_item_1_delivery_date_month'))
		delivery_date_month.select_by_value(str(delivery_date.month))

		if description2:
			form.find_element_by_id('item_2_description_input').send_keys(description2)
			form.find_element_by_id('item_2_fullname_input').send_keys(fullname2)
			form.find_element_by_id('item_2_price_input').send_keys(price2)
			form_job = Select(form.find_element_by_id('item_2_job_input'))
			form_job.select_by_value(job2.address)
			form_delivery_location = Select(form.find_element_by_id('item_2_delivery_location_input'))
			form_delivery_location.select_by_value(delivery_location2)
			form.find_element_by_id('item_2_quantity_input').send_keys(quantity2)
	
			delivery_date_day=Select(form.find_element_by_id('id_item_2_delivery_date_day'))
			delivery_date_day.select_by_value(str(delivery_date2.day))
	
			delivery_date_year=Select(form.find_element_by_id('id_item_2_delivery_date_year'))
			delivery_date_year.select_by_value(str(delivery_date2.year))
	
			delivery_date_month=Select(form.find_element_by_id('id_item_2_delivery_date_month'))
			delivery_date_month.select_by_value(str(delivery_date2.month))

		if description3:
			form.find_element_by_id('item_3_description_input').send_keys(description3)
			form.find_element_by_id('item_3_fullname_input').send_keys(fullname3)
			form.find_element_by_id('item_3_price_input').send_keys(price3)
			form_job = Select(form.find_element_by_id('item_3_job_input'))
			form_job.select_by_value(job3.address)
			form_delivery_location = Select(form.find_element_by_id('item_3_delivery_location_input'))
			form_delivery_location.select_by_value(delivery_location3)
			form.find_element_by_id('item_3_quantity_input').send_keys(quantity3)
	
			delivery_date_day=Select(form.find_element_by_id('id_item_3_delivery_date_day'))
			delivery_date_day.select_by_value(str(delivery_date3.day))
	
			delivery_date_year=Select(form.find_element_by_id('id_item_3_delivery_date_year'))
			delivery_date_year.select_by_value(str(delivery_date3.year))
	
			delivery_date_month=Select(form.find_element_by_id('id_item_3_delivery_date_month'))
			delivery_date_month.select_by_value(str(delivery_date3.month))

		if description4:
			form.find_element_by_id('item_4_description_input').send_keys(description4)
			form.find_element_by_id('item_4_fullname_input').send_keys(fullname4)
			form.find_element_by_id('item_4_price_input').send_keys(price4)
			form_job = Select(form.find_element_by_id('item_4_job_input'))
			form_job.select_by_value(job4.address)
			form_delivery_location = Select(form.find_element_by_id('item_4_delivery_location_input'))
			form_delivery_location.select_by_value(delivery_location4)
			form.find_element_by_id('item_4_quantity_input').send_keys(quantity4)
	
			delivery_date_day=Select(form.find_element_by_id('id_item_4_delivery_date_day'))
			delivery_date_day.select_by_value(str(delivery_date4.day))
	
			delivery_date_year=Select(form.find_element_by_id('id_item_4_delivery_date_year'))
			delivery_date_year.select_by_value(str(delivery_date4.year))
	
			delivery_date_month=Select(form.find_element_by_id('id_item_4_delivery_date_month'))
			delivery_date_month.select_by_value(str(delivery_date4.month))

		if description5:
			form.find_element_by_id('item_5_description_input').send_keys(description5)
			form.find_element_by_id('item_5_fullname_input').send_keys(fullname5)
			form.find_element_by_id('item_5_price_input').send_keys(price5)
			form_job = Select(form.find_element_by_id('item_5_job_input'))
			form_job.select_by_value(job5.address)
			form_delivery_location = Select(form.find_element_by_id('item_5_delivery_location_input'))
			form_delivery_location.select_by_value(delivery_location5)
			form.find_element_by_id('item_5_quantity_input').send_keys(quantity5)
	
			delivery_date_day=Select(form.find_element_by_id('id_item_5_delivery_date_day'))
			delivery_date_day.select_by_value(str(delivery_date5.day))
	
			delivery_date_year=Select(form.find_element_by_id('id_item_5_delivery_date_year'))
			delivery_date_year.select_by_value(str(delivery_date5.year))
	
			delivery_date_month=Select(form.find_element_by_id('id_item_5_delivery_date_month'))
			delivery_date_month.select_by_value(str(delivery_date5.month))

		if description6:
			form.find_element_by_id('item_6_description_input').send_keys(description6)
			form.find_element_by_id('item_6_fullname_input').send_keys(fullname6)
			form.find_element_by_id('item_6_price_input').send_keys(price6)
			form_job = Select(form.find_element_by_id('item_6_job_input'))
			form_job.select_by_value(job6.address)
			form_delivery_location = Select(form.find_element_by_id('item_6_delivery_location_input'))
			form_delivery_location.select_by_value(delivery_location6)
			form.find_element_by_id('item_6_quantity_input').send_keys(quantity6)
	
			delivery_date_day=Select(form.find_element_by_id('id_item_6_delivery_date_day'))
			delivery_date_day.select_by_value(str(delivery_date6.day))
	
			delivery_date_year=Select(form.find_element_by_id('id_item_6_delivery_date_year'))
			delivery_date_year.select_by_value(str(delivery_date6.year))
	
			delivery_date_month=Select(form.find_element_by_id('id_item_6_delivery_date_month'))
			delivery_date_month.select_by_value(str(delivery_date6.month))

		if description7:
			form.find_element_by_id('item_4_description_input').send_keys(description4)
			form.find_element_by_id('item_4_fullname_input').send_keys(fullname4)
			form.find_element_by_id('item_4_price_input').send_keys(price4)
			form_job = Select(form.find_element_by_id('item_4_job_input'))
			form_job.select_by_value(job4.address)
			form_delivery_location = Select(form.find_element_by_id('item_4_delivery_location_input'))
			form_delivery_location.select_by_value(delivery_location4)
			form.find_element_by_id('item_4_quantity_input').send_keys(quantity4)
	
			delivery_date_day=Select(form.find_element_by_id('id_item_4_delivery_date_day'))
			delivery_date_day.select_by_value(str(delivery_date4.day))
	
			delivery_date_year=Select(form.find_element_by_id('id_item_4_delivery_date_year'))
			delivery_date_year.select_by_value(str(delivery_date4.year))
	
			delivery_date_month=Select(form.find_element_by_id('id_item_4_delivery_date_month'))
			delivery_date_month.select_by_value(str(delivery_date4.month))

		if description8:
			form.find_element_by_id('item_8_description_input').send_keys(description8)
			form.find_element_by_id('item_8_fullname_input').send_keys(fullname8)
			form.find_element_by_id('item_8_price_input').send_keys(price8)
			form_job = Select(form.find_element_by_id('item_8_job_input'))
			form_job.select_by_value(job8.address)
			form_delivery_location = Select(form.find_element_by_id('item_8_delivery_location_input'))
			form_delivery_location.select_by_value(delivery_location8)
			form.find_element_by_id('item_8_quantity_input').send_keys(quantity8)
	
			delivery_date_day=Select(form.find_element_by_id('id_item_8_delivery_date_day'))
			delivery_date_day.select_by_value(str(delivery_date8.day))
	
			delivery_date_year=Select(form.find_element_by_id('id_item_8_delivery_date_year'))
			delivery_date_year.select_by_value(str(delivery_date8.year))
	
			delivery_date_month=Select(form.find_element_by_id('id_item_8_delivery_date_month'))
			delivery_date_month.select_by_value(str(delivery_date8.month))

		if description9:
			form.find_element_by_id('item_9_description_input').send_keys(description9)
			form.find_element_by_id('item_9_fullname_input').send_keys(fullname9)
			form.find_element_by_id('item_9_price_input').send_keys(price9)
			form_job = Select(form.find_element_by_id('item_9_job_input'))
			form_job.select_by_value(job9.address)
			form_delivery_location = Select(form.find_element_by_id('item_9_delivery_location_input'))
			form_delivery_location.select_by_value(delivery_location9)
			form.find_element_by_id('item_9_quantity_input').send_keys(quantity9)
	
			delivery_date_day=Select(form.find_element_by_id('id_item_9_delivery_date_day'))
			delivery_date_day.select_by_value(str(delivery_date9.day))
	
			delivery_date_year=Select(form.find_element_by_id('id_item_9_delivery_date_year'))
			delivery_date_year.select_by_value(str(delivery_date9.year))
	
			delivery_date_month=Select(form.find_element_by_id('id_item_9_delivery_date_month'))
			delivery_date_month.select_by_value(str(delivery_date9.month))

		if description10:
			form.find_element_by_id('item_10_description_input').send_keys(description10)
			form.find_element_by_id('item_10_fullname_input').send_keys(fullname10)
			form.find_element_by_id('item_10_price_input').send_keys(price10)
			form_job = Select(form.find_element_by_id('item_10_job_input'))
			form_job.select_by_value(job10.address)
			form_delivery_location = Select(form.find_element_by_id('item_10_delivery_location_input'))
			form_delivery_location.select_by_value(delivery_location10)
			form.find_element_by_id('item_10_quantity_input').send_keys(quantity10)
	
			delivery_date_day=Select(form.find_element_by_id('id_item_10_delivery_date_day'))
			delivery_date_day.select_by_value(str(delivery_date10.day))
	
			delivery_date_year=Select(form.find_element_by_id('id_item_10_delivery_date_year'))
			delivery_date_year.select_by_value(str(delivery_date10.year))
	
			delivery_date_month=Select(form.find_element_by_id('id_item_10_delivery_date_month'))
			delivery_date_month.select_by_value(str(delivery_date10.month))

		self.click(base_element='PO_panel', element='PO_panel_PO_form_submit_button')
		self.wait_for(lambda: self.assertTrue(self.browser.find_element_by_id('site_management_panel').is_displayed()))

	def create_schedule_item(self, name, date1, quantity, job, date2=None):
		self.browser.get(self.live_server_url+reverse('job', kwargs={'job_id':job.job_id}))
		self.wait_until_visible('schedule_of_items_panel')

		self.browser.find_element_by_id('schedule_item_name_input').send_keys(name)
		self.browser.find_element_by_id('schedule_item_quantity_input').send_keys(quantity)

		month1 = Select(self.browser.find_element_by_id('id_date_1_month'))
		month1.select_by_value(str(date1.month))
		day1 = Select(self.browser.find_element_by_id('id_date_1_day'))
		day1.select_by_value(str(date1.day))
		year1 = Select(self.browser.find_element_by_id('id_date_1_year'))
		year1.select_by_value(str(date1.year))


		if date2:
			month2 = Select(self.browser.find_element_by_id('id_date_2_month'))
			month2.select_by_value(str(date2.month))
			day2 = Select(self.browser.find_element_by_id('id_date_2_day'))
			day2.select_by_value(str(date2.day))
			year2 = Select(self.browser.find_element_by_id('id_date_2_year'))
			year2.select_by_value(str(date2.year))

		ActionChains(self.browser).click(self.browser.find_element_by_id('schedule_item_add_button')).perform()
		new_schedule_item = Scheduled_items.objects.filter(description=name).first()
		self.wait_until_visible(f'schedule_item_{new_schedule_item.pk}')
	#-- SETUP AND TEARDOWN --#

	# need to set up:
	# Job 1: # all of these are plus one so as to differentiate between the whole job deletion and the manual deletes #job 1 for manual deletes, job 2 will be totally deleted
		# 2 shopping list items # make sure only one is deleted in unittests 
		# 2 purchase order item # make sure only one is deleted in unittests
		# 2 acquired shopping list item (item with no P.O)#
		# 4 Job notes (two for job view, two for home page)

	# Job 2:
		# 3 Note
		# 3 Scheduled item
		# purchase order no.1:
			# 3 Purchase Order items
		# purchase order no.2:
			# 3 Purchase Order items
		# 3 acquired shopping list items
		# 3 shopping list items

	# extras:
		# 2 admin notes on homepage

	def setUp(self):
		with self.settings(NOW = date(year=2017, month=1, day=2)): # stops the tests screwing up, make sure now is a monday (so now + a few days == later THIS week)
			now = settings.NOW
			Site_info.objects.create(locked=False, password='thischangesautomaticallyaftereverylock')
			self.browser = webdriver.Chrome()
			self.login(self.browser)

			# Job 1
			self.create_custom_job(name='Tony Stark', email='TonyS@StarkIndustries.com', phone='01234567898', address='200 Park Avenue', note='This is job 1')
			job1 = Jobs.objects.filter(address='200 Park Avenue').first()
			
			# Job 1 - shopping list item 1 and 2
			self.add_shopping_list_item('job 1 shopping list item 1', 1, job1)
			self.add_shopping_list_item('job 1 shopping list item 2', 1, job1)

			# Job 1 - acquired shopping list items 1 and 2
			self.add_acquired_shopping_list_item('job 1 - acquired shopping list item 1', 1, job1)
			self.add_acquired_shopping_list_item('job 1 - acquired shopping list item 2', 1, job1)
			
			# Job 1 - Purchase order items 1 and 2
			self.create_purchase_order(
				description = 'job 1 - purchase order 1 - item 1 description',
				fullname = 'job 1 - purchase order 1 - item 1 fullname',
				delivery_date= now,
				job = job1,

				description2 = 'job 1 - purchase order 1 - item 2 description' ,
				fullname2 = 'job 1 - purchase order 1 - item 2 fullname',
				delivery_date2= now,
				job2 = job1,
				quantity2 = 1,
				price2 = 100,
				delivery_location2= 'shop'
				)

			# Job 1 - job notes 1-4
			self.add_job_note('job 1 title 1', 'job 1 text 1', job1)
			self.add_job_note('job 1 title 2', 'job 1 text 2', job1)
			self.add_job_note('job 1 title 3', 'job 1 text 3', job1)
			self.add_job_note('job 1 title 4', 'job 1 text 4', job1)


			# Job 2
			self.create_custom_job(name='Adam Jensen', email='Adam.Jensen@si.det.usa', address='601 Chiron Building', phone='01234567898', note='This is job 2')
			job2 = Jobs.objects.filter(address='601 Chiron Building').first()

			# Job 2 notes 1-3
			self.add_job_note('job 2 title 1', 'job 2 text 1', job2)
			self.add_job_note('job 2 title 2', 'job 2 text 2', job2)
			self.add_job_note('job 2 title 3', 'job 2 text 3', job2)

			# Job 2 schedule item 1-3
			self.create_schedule_item('job 2 - schedule item 1', now, 1, job2)
			self.create_schedule_item('job 2 - schedule item 2', now, 1, job2)
			self.create_schedule_item('job 2 - schedule item 3', now, 1, job2)

			# Job 2 Purchase order 1 items 1-3
			self.create_purchase_order(
				supplier_ref = 'job 2 po 1',
				description = 'job 2 - purchase order 1 - item 1 description',
				fullname = 'job 2 - purchase order 1 - item 1 fullname',
				delivery_date= now,
				job = job2,

				description2 = 'job 2 - purchase order 1 - item 2 description' ,
				fullname2 = 'job 2 - purchase order 1 - item 2 fullname',
				delivery_date2= now,
				job2 = job2,
				quantity2 = 1,
				price2 = 100,
				delivery_location2= 'shop',

				description3 = 'job 2 - purchase order 1 - item 3 description' ,
				fullname3 = 'job 2 - purchase order 1 - item 3 fullname',
				delivery_date3= now,
				job3 = job2,
				quantity3 = 1,
				price3 = 100,
				delivery_location3= 'shop',
				)

			# Job 2 Purchase order 2 items 1-3
			self.create_purchase_order(
				supplier_ref = 'job 2 po 2',
				description = 'job 2 - purchase order 2 - item 1 description',
				fullname = 'job 2 - purchase order 2 - item 1 fullname',
				delivery_date= now,
				job = job2,

				description2 = 'job 2 - purchase order 2 - item 2 description' ,
				fullname2 = 'job 2 - purchase order 2 - item 2 fullname',
				delivery_date2= now,
				job2 = job2,
				quantity2 = 1,
				price2 = 100,
				delivery_location2= 'shop',

				description3 = 'job 2 - purchase order 2 - item 3 description' ,
				fullname3 = 'job 2 - purchase order 2 - item 3 fullname',
				delivery_date3= now,
				job3 = job2,
				quantity3 = 1,
				price3 = 100,
				delivery_location3= 'shop',
				)

			# Job 2 acquired shopping list items 1-3
			self.add_acquired_shopping_list_item('job 2 - acquired shopping list item 1', 1, job2)
			self.add_acquired_shopping_list_item('job 2 - acquired shopping list item 2', 1, job2)
			self.add_acquired_shopping_list_item('job 2 - acquired shopping list item 3', 1, job2)

			# Job 2 shopping list items 1-3
			self.add_shopping_list_item('job 2 shopping list item 1', 1, job2)
			self.add_shopping_list_item('job 2 shopping list item 2', 1, job2)


			# admin notes 1 and 2
			self.add_admin_note('admin note 1 title', 'admin note 1 text')
			self.add_admin_note('admin note 2 title', 'admin note 2 text')

		# ENSURE ALL SHOPPING LIST ITEMS ARE UNIQUE THROUGOUT THIS ENTIRE TEST
		# ENSURE ALL NOTES ARE UNIQUE THROUGHOUT THIS ENTIRE TEST
		# ENSURE ALL SCHEDULE ITEM NAMES ARE UNIQUE THROUGHOUT THIS ENTIRE TEST

	##############################################################################################################
	##############################################################################################################
	##############################################################################################################
	##############################################################################################################
	##############################################################################################################
	##############################################################################################################

	# job 1 will have all the stuff individually deleted
	# job 2 is the job that gets deleted as a whole

	def test_deletion_sequence(self):

		#-- Notes --#
	
		# Marek sees a note he wants to delete in JOB 1 VIEW (200 Park Avenue)
		self.browser.get(self.live_server_url+reverse('job', kwargs={'job_id':'200ParkAvenue'}))
		self.wait_until_visible('notes_panel')
		job_view_note_to_delete = Notes.objects.filter(Title='job 1 title 1').first()
		job_view_note_to_preserve = Notes.objects.filter(Title='job 1 title 2').first()
	
		# Marek clicks the 'del' hyperlink at the very bottom of the notes text of the note he wants to delete
		self.click(base_element=f'Note_{job_view_note_to_delete.pk}', element='delete_note_button')
		
		# The page refreshes and the note is gone
		self.wait_for(lambda: self.assertEqual(self.live_server_url+reverse('job', kwargs={'job_id':'200ParkAvenue'}), self.browser.current_url))
		self.wait_for(lambda: self.assertNotIn('job 1 title 1', self.browser.page_source)) # REFRACT - compare element source not whole page
		self.wait_for(lambda: self.assertIn('job 1 title 2', self.browser.page_source))
	
		
		# Marek sees a job note he wants to delete on the HOME PAGE
		self.browser.get(self.live_server_url+reverse('homepage'))
		self.wait_until_visible('notes_panel')
		home_page_note_to_delete = Notes.objects.filter(Title='job 1 title 3').first()
		home_page_note_to_preserve = Notes.objects.filter(Title='job 1 title 4').first()
	
		# Marek clicks the 'all jobs' panel
		self.click('all_notes_panel_toggle')
		self.wait_until_visible('all_notes_panel')
		# Marek clicks the 'del' hyperlink at the very bottom of the notes text
		self.click(base_element=f'Note_{home_page_note_to_delete.pk}', element='delete_note_button')
		
		# The page refreshes and the note is gone
		self.wait_for(lambda: self.assertEqual(self.live_server_url+reverse('homepage'), self.browser.current_url))
		self.wait_for(lambda: self.assertNotIn('job 1 title 3', self.browser.page_source)) # REFRACT - compare element source not whole page
		self.assertIn('job 1 title 4', self.browser.page_source)
	
		
		# Marek clicks to see the admin notes
		self.click('admin_notes_panel_toggle')
		self.wait_until_visible('admin_notes_panel')
		# Marek sees an admin note he wants to delete on the HOME PAGE
		admin_note_to_delete = Notes.objects.filter(Title='admin note 1 title').first()
		admin_note_to_preserve = Notes.objects.filter(Title='admin note 2 title').first()
	
		# Marek clicks the 'del' hyperlink at the very bottom of the notes text
		self.click(base_element=f'Note_{admin_note_to_delete.pk}', element='delete_note_button')
		
		# The page refreshes and the note is gone
		self.wait_for(lambda: self.assertEqual(self.live_server_url+reverse('homepage'), self.browser.current_url))
		self.wait_for(lambda: self.assertNotIn('admin note 1 title', self.browser.page_source)) # REFRACT - compare element source not whole page
		self.assertIn('admin note 2 title', self.browser.page_source)
	
	
	
		#-- Shopping list items --#
	
		# Marek sees a shopping list item he wants to delete in the SHOPPING LIST PAGE
		self.browser.get(self.live_server_url+reverse('shopping_list'))
		self.wait_until_visible('shopping_list_panel')
		shopping_list_page_item_to_delete = Shopping_list_items.objects.filter(description='job 1 shopping list item 1').first()
		shopping_list_page_item_to_preserve = Shopping_list_items.objects.filter(description='job 1 shopping list item 2').first() # REFRACT - is this line being used? check in all other deletions too
	
		# Marek clicks the 'del' hyperlink on the far right of the item
		self.click(base_element=f'Shopping_list_items_{shopping_list_page_item_to_delete.pk}', element='delete_shopping_list_item_button')
	
		# The page refreshes and the item is gone
		self.wait_for(lambda: self.assertEqual(self.live_server_url+reverse('shopping_list'), self.browser.current_url))
		self.wait_for(lambda: self.assertNotIn('job 1 shopping list item 1', self.browser.page_source))
		self.assertIn('job 1 shopping list item 2', self.browser.page_source)
	
	
		# Marek sees a shopping list item he wants to delete in the HOME 
		self.browser.get(self.live_server_url+reverse('homepage'))
		self.wait_until_visible('shopping_list_panel')
		home_page_shopping_list_item_to_delete = Shopping_list_items.objects.filter(description='job 1 shopping list item 2').first()
	
		# Marek clicks the 'del' hyperlink on the far right of the item
		self.click(base_element=f'Shopping_list_items_{home_page_shopping_list_item_to_delete.pk}', element='delete_shopping_list_item_button')
		
		# The page refreshes and the item is gone
		self.wait_for(lambda: self.assertEqual(self.live_server_url+reverse('homepage'), self.browser.current_url))
		self.wait_for(lambda: self.assertNotIn('job 1 shopping list item 2', self.browser.page_source))
	
		
	
		#-- Purchase Order items --#
	
		# Marek sees an item he wants to delete
		self.browser.get(self.live_server_url+reverse('job', kwargs={'job_id':'200ParkAvenue'}))
		self.wait_until_visible('site_management_panel')
		self.click('en_route_panel_toggle')
		self.wait_until_visible('en_route_panel')
		purchase_order_item_to_delete = Items.objects.filter(description = 'job 1 - purchase order 1 - item 1 description').first()
	
		# He clicks on the items name and is redirected to the purchase order view in which the item is contained
		self.click(f'po_link_item_{purchase_order_item_to_delete.pk}')
		self.wait_for(lambda: self.assertEqual(self.live_server_url+reverse('purchase_orders', kwargs={'order_no':purchase_order_item_to_delete.PO.order_no}), self.browser.current_url))
		purchase_order_url = self.browser.current_url
		# on the far right hand side of the item's row is a 'del' hyperlink. he clicks it, the page refreshes and the item is delieted
		self.click(base_element=f'PO_item_{purchase_order_item_to_delete.pk}', element='delete_po_item_button')
		self.wait_for(lambda: self.assertEqual(purchase_order_url, self.browser.current_url))
		self.wait_for(lambda: self.assertNotIn(f'PO_item_{purchase_order_item_to_delete.pk}', self.browser.page_source))
	
		
		
		#-- Items objects with no purchase orders (acquired shopping list items) --#
		
		# Marek sees an acquired shopping list item in the 'en-route' section of a job he wishes to delete
		self.browser.get(self.live_server_url+reverse('job', kwargs={'job_id':'200ParkAvenue'}))
		self.wait_until_visible('site_management_panel')
		self.click('en_route_panel_toggle')
		self.wait_until_visible('en_route_panel')
		acquired_shopping_list_item_to_delete = Items.objects.filter(description='job 1 - acquired shopping list item 1').first()
	
		# Marek clicks the small 'del' hyperlink on the far right of the item
		self.click(base_element=f'en_route_item_{acquired_shopping_list_item_to_delete.pk}', element='delete_item_button') #item.model = acquired, if model == 'acquired' render del button
		# The page refreshes and the item is no longer there
		self.wait_for(lambda: self.assertEqual(self.live_server_url+reverse('job', kwargs={'job_id':'200ParkAvenue'}), self.browser.current_url))
		self.wait_for(lambda: self.assertNotIn(f'en_route_item_{acquired_shopping_list_item_to_delete.pk}', self.browser.page_source))
	
		



		#-- Job --#
	
		# in the jobs view marek sees a dropdown menu in the top right corner where there's a link saying 'delete job'
		self.browser.get(self.live_server_url + reverse('jobs'))
		self.wait_until_visible('all_jobs_panel')
	
		self.click('jobsDropdownMenuButton')
		self.wait_until_visible('jobsDropDown')
	
		# clicking this redirects to a delete job page
		self.click('delete_job_page_link')
		# here David sees a warning saying:
		#  "WARNING - THIS WILL PERMANENTLY DELETE EVERYTHING LINKED TO THIS JOB. EVERY ITEM, NOTE, SHOPPING LIST, PURCHASE ORDER, SCHEDULED ITEM - EVERYTHING - THERE IS NO UNDOING THIS DELETE"
	
		# David sees a dropdown menu from which he selects job2 to delete (601 Chiron Building)
		delete_job_choice = Select(self.browser.find_element_by_id('delete_job_choice_input'))
		delete_job_choice.select_by_value('601 Chiron Building')
		# He sees another two fields saying something along the lines of 'you must type the address of this job twice correcly in order to delete'. He fills this out incorrectly
		self.browser.find_element_by_id('security_field_1').send_keys('601 Chiron Building')
		self.browser.find_element_by_id('security_field_2').send_keys('incorrect string')
		# He hits submit - the page refreshes with an alert saying 'security fields did not match'
		self.click('delete_job_form_submit_button')
	
		self.wait_for(lambda: self.assertIn('security fields did not match, nothing deleted', self.browser.page_source))
		
		# He types it correctly this time, hits submit and finds everything to do with the job deleted.
		delete_job_choice = Select(self.browser.find_element_by_id('delete_job_choice_input'))
		delete_job_choice.select_by_value('601 Chiron Building')
		self.browser.find_element_by_id('security_field_1').send_keys('601 Chiron Building')
		self.browser.find_element_by_id('security_field_2').send_keys('601 Chiron Building')

		self.click('delete_job_form_submit_button')
	
		self.wait_for(lambda: self.assertIn('601 Chiron Building JOB DELETED', self.browser.page_source))
	
		# He checks all over the system and, indeed, every trace of the 601 Chiron Building job is no longer there
	
		# checks jobs
		self.browser.get(self.live_server_url+reverse('jobs'))
		self.wait_for(lambda: self.assertNotIn('601 Chiron Building', self.browser.page_source)) # check if this checks the html even if the thing isn't visible
	
		# checks all notes on homepage
		self.browser.get(self.live_server_url+reverse('homepage'))
		self.wait_for(lambda: self.assertNotIn('job 2 title 1', self.browser.page_source))
		self.assertNotIn('job 2 title 2', self.browser.page_source)
		self.assertNotIn('job 2 title 3', self.browser.page_source)
	
		# checks shopping list
		self.browser.get(self.live_server_url+reverse('shopping_list'))
		self.wait_for(lambda: self.assertNotIn('job 2 shopping list item 1', self.browser.page_source))
		self.assertNotIn('job 2 shopping list item 2', self.browser.page_source)
	
		# However the purchase orders and related items remain
		job2_purchase_order_1 = Purchase_orders.objects.filter(supplier_ref='job 2 po 1').first()
		job2_purchase_order_2 = Purchase_orders.objects.filter(supplier_ref='job 2 po 2').first()
	
		self.browser.get(self.live_server_url+reverse('purchase_orders', kwargs={'order_no':job2_purchase_order_1.order_no}))
		self.wait_until_visible('purchase_order_table')
	
		self.assertIn('601 Chiron Building', self.browser.find_element_by_id('purchase_order_table').get_attribute("innerHTML"))
	
		self.browser.get(self.live_server_url+reverse('purchase_orders', kwargs={'order_no':job2_purchase_order_2.order_no}))
		self.wait_until_visible('purchase_order_table')
	
		self.assertIn('601 Chiron Building', self.browser.find_element_by_id('purchase_order_table').get_attribute("innerHTML"))

