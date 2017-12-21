from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from django.urls import reverse
from selenium.webdriver.support.ui import Select
from django.conf import settings
from dateutil.relativedelta import relativedelta
import datetime
from datetime import date
import time

from Home_Panel.views import convert_to_date

from _Auth.models import Site_info
from Jobs.models import Jobs
from Notes.models import Notes
from Item_Flow.models import Scheduled_items, Purchase_orders, Items
from Shopping_list.models import Shopping_list_items


homepage_elements = [
		'parent_deliveries_panel', 'today_deliveries_panel_toggle', 'this_week_deliveries_panel_toggle', 'all_deliveries_panel_toggle',
		'today_deliveries_panel', 'this_week_deliveries_panel', 'all_deliveries_panel', 'shopping_list_panel', 'notes_panel', 'admin_notes_panel_toggle',
		'all_notes_panel_toggle', 'admin_notes_panel', 'all_notes_panel', 'new_note_form', 'PO_panel',
		]

shopping_list_elements = ['shopping_list_panel', 'new_shopping_list_item_form',]

jobs_elements = [
		'jobsDropdownMenuButton', 'jobsDropDown', 'all_jobs_panel', 'ongoing_jobs_panel_toggle', 'completed_jobs_panel_toggle', 'quote_jobs_panel_toggle',
		'ongoing_jobs_panel', 'completed_jobs_panel', 'quote_jobs_panel', 'create_job_button',
		]

jobs_elements_manager_excluded = ['delete_job_page_link',]

job_elements = [
		'Profile', 'status_menu_toggle', 'status_menu', 'Quote_status_change', 'Ongoing_status_change', 'Completed_status_change', 'notes_panel', 'new_note_form',
		'schedule_of_items_panel', 'site_management_panel', 'en_route_panel_toggle', 'on_site_panel_toggle', 'PO_panel_toggle',
		'en_route_panel', 'on_site_panel', 'PO_panel',
		]



class PermissionsTest(FunctionalTest):

	# any object where the permission needs to be restricted in any way MUST be tested here

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

	def assert_not_visible(self, element, base_element=None): # - REFRACT, may need to change this to say 'assert_not_rendered'
		if base_element:
			return self.wait_for(lambda: self.assertNotIn(f'id="{element}"', self.browser.find_element_by_id(base_element).get_attribute("innerHTML")))
		else:
			return self.wait_for(lambda: self.assertNotIn(f'id="{element}"', self.browser.page_source))

	def create_custom_job(self, name, email, phone, address, note):
		self.browser.get(self.live_server_url+reverse('jobs'))
		self.click('quote_jobs_panel_toggle')
		self.wait_until_visible('quote_jobs_panel')
		self.click('create_job_button')
		self.wait_until_visible('Name')
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
		self.wait_for(lambda: self.assertIn(title, self.browser.page_source))

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

	def slow_type(self, element, string, base_element=None):
		if base_element:
			time.sleep(0.5)
			if base_element:
				for char in string:
					time.sleep(0.1)
					self.browser.find_element_by_id(base_element).find_element_by_id(element).send_keys(str(char))
			else:
				for char in string:
					time.sleep(0.1)
					self.browser.find_element_by_id(element).send_keys(str(char))

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
			form.find_element_by_id('item_7_description_input').send_keys(description7)
			form.find_element_by_id('item_7_fullname_input').send_keys(fullname7)
			form.find_element_by_id('item_7_price_input').send_keys(price7)
			form_job = Select(form.find_element_by_id('item_7_job_input'))
			form_job.select_by_value(job7.address)
			form_delivery_location = Select(form.find_element_by_id('item_7_delivery_location_input'))
			form_delivery_location.select_by_value(delivery_location7)
			form.find_element_by_id('item_7_quantity_input').send_keys(quantity7)
	
			delivery_date_day=Select(form.find_element_by_id('id_item_7_delivery_date_day'))
			delivery_date_day.select_by_value(str(delivery_date7.day))
	
			delivery_date_year=Select(form.find_element_by_id('id_item_7_delivery_date_year'))
			delivery_date_year.select_by_value(str(delivery_date7.year))
	
			delivery_date_month=Select(form.find_element_by_id('id_item_7_delivery_date_month'))
			delivery_date_month.select_by_value(str(delivery_date7.month))

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

	def wait_for_url(self, url):
		self.wait_for(lambda: self.assertEqual(url, self.browser.current_url))

	def go_to(self, reverse):
		self.browser.get(self.live_server_url+reverse)

	def accept_delivery(self, item):
		# this assumes you are already on the home page and the accept delivery button is visible
		self.click(f'accept_delivery_button_{item.pk}')
		self.wait_for(lambda: self.assertNotIn(f'accept_delivery_button_{item.pk}', self.browser.page_source))

	def reject_and_reschedule(self, item):
		# this assumes you are on the home page and the reject delivery button is visible
		delivery_date = convert_to_date(item.delivery_date)

		self.click(f'reject_delivery_button_{item.pk}')
		self.wait_until_visible(f'delivery_rejection_modal')

		delivery_rejection_form = self.browser.find_element_by_id(f'delivery_rejection_modal_{item.pk}').find_element_by_id('delivery_rejection_form')			
		delivery_rejection_form.find_element_by_id('id_note').send_keys('item is damaged')
		
		reschedule_date_year = Select(delivery_rejection_form.find_element_by_id('id_reschedule_date_year'))
		reschedule_date_year.select_by_value(str(delivery_date.year))
		
		reschedule_date_day = Select(delivery_rejection_form.find_element_by_id('id_reschedule_date_day'))
		reschedule_date_day.select_by_value(str(delivery_date.day+2))
		
		reschedule_date_month = Select(delivery_rejection_form.find_element_by_id('id_reschedule_date_month'))
		reschedule_date_month.select_by_value(str(delivery_date.month))
		
		self.click(base_element=f'delivery_rejection_modal_{item.pk}', element='reject_delivery_form_submit')
		self.wait_for(lambda: self.assertIn(f'{item.description} rejected', self.browser.page_source))

	def reject_and_cancel(self, item):
		# this assumes you are on the home page and the reject delivery button is visible
		self.click(f'reject_delivery_button_{item.pk}')
		self.wait_until_visible(f'delivery_rejection_modal_{item.pk}')
		delivery_rejection_form = self.browser.find_element_by_id(f'delivery_rejection_modal_{item.pk}').find_element_by_id('delivery_rejection_form')			
		delivery_rejection_form.find_element_by_id('id_note').send_keys('item is damaged')
		self.click(base_element=f'delivery_rejection_modal_{item.pk}', element='reject_delivery_form_submit')
		self.wait_for(lambda: self.assertIn(f'{item.description} rejected', self.browser.page_source))

	def click_menu_button(self):
		ActionChains(self.browser).click(self.browser.find_element_by_id('status_menu_toggle')).perform()

	












	#-- SETUP --#

	def setUp(self):

		# make sure the job it makes sync's up EXACTLY with deletes.py functional test so the C+P works.

		with self.settings(NOW = date(year=2017, month=1, day=2)): # stops the tests screwing up, make sure now is a monday (so now + a few days == later THIS week)
			now = settings.NOW
			twodays = now+relativedelta(days=2)
			twoweeks = now+relativedelta(weeks=2)
			self.setup_system()
			self.loginSuper()

			# admin notes
			self.add_admin_note('admin note 1 title', 'admin note 1 text')
			self.add_admin_note('admin note 2 title', 'admin note 2 text')

			# Job 1
			self.create_custom_job(name='Tony Stark', email='TonyS@StarkIndustries.com', phone='01234567898', address='200 Park Avenue', note='This is job 1')
			job1 = Jobs.objects.filter(address='200 Park Avenue').first()
			# Make job 1 an ongoing job
			self.click('status_menu_toggle')
			self.wait_until_visible('status_menu')
			self.click('Ongoing_status_change')
			self.wait_for(lambda: self.assertIn('ULTRAMARINE_BLUE_PROFILE_BOX', self.browser.page_source))

			# Job 2 manager R quote jobs test
			self.create_custom_job(name='R quote jobs test', email='asdf@asdf.com', phone='01234567898', address='1 test street', note='manager R quote jobs test')

			# Job 3 manager R ongoing jobs test
			self.create_custom_job(name='R ongoing jobs test', email='asdf@asdf.com', phone='01234567898', address='2 test street', note='manager R ongoing jobs test')
			self.click('status_menu_toggle')
			self.wait_until_visible('status_menu')
			self.click('Ongoing_status_change')
			self.wait_for(lambda: self.assertIn('ULTRAMARINE_BLUE_PROFILE_BOX', self.browser.page_source))

			# Job 4 manager R completed jobs test
			self.create_custom_job(name='R completed jobs test', email='asdf@asdf.com', phone='01234567898', address='3 test street', note='manager R completed jobs test')
			self.click_menu_button()
			self.click('Completed_status_change')	
			self.wait_for(lambda: self.assertIn('FAINT_BLUE_PROFILE_BOX', self.browser.page_source))

			# Job 5 manager U job statuses test
			self.create_custom_job(name='U statuses jobs test', email='asdf@asdf.com', phone='01234567898', address='4 test street', note='manager U job statuses test')

			# Job 1 - job notes 1-4
			self.add_job_note('job 1 title 1', 'job 1 text 1', job1)
			self.add_job_note('job 1 title 2', 'job 1 text 2', job1)
			self.add_job_note('job 1 title 3', 'job 1 text 3', job1)
			self.add_job_note('job 1 title 4', 'job 1 text 4', job1)


			# Job 1 - shopping list item 1 and 2
			self.add_shopping_list_item('job 1 shopping list item 1', 1, job1)
			self.add_shopping_list_item('job 1 shopping list item 2', 1, job1)

			# Job 1 - acquired shopping list items 1 and 2
			self.add_acquired_shopping_list_item('job 1 - acquired shopping list item 1', 1, job1) # DELETES TEST
			self.add_acquired_shopping_list_item('job 1 - acquired shopping list item 2', 1, job1) # DELETES TEST

			self.add_acquired_shopping_list_item('job 1 - acquired shopping list item 1 staff', 1, job1) # STAFF TEST
			self.add_acquired_shopping_list_item('job 1 - acquired shopping list item 2 staff', 1, job1) # STAFF TEST

			self.add_acquired_shopping_list_item('job 1 - acquired shopping list item 1 manager', 1, job1) # MANAGER TEST
			self.add_acquired_shopping_list_item('job 1 - acquired shopping list item 2 manager', 1, job1) # MANAGER TEST
			
			# Job 1 - scheduled items || manager crud testing
			self.create_schedule_item('job 1 - scheduled item 1 manager', now, 1, job1)

			# Job 1 - Purchase order items 1 and 2 || DELETES TEST
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

			# Job 1 - Purchase order items for staff CRU permissions test HOMEPAGE
			self.create_purchase_order(
				description = 't a d', # today accept description
				fullname = 't a f', # today accept fullname
				delivery_date = now,
				job = job1,

				description2 = 't r r d', #today reject and reschedule
				fullname2 = 't r r f',
				delivery_date2 = now,
				job2 = job1,
				quantity2 = 1,
				price2 = 100,
				delivery_location2 = 'shop',

				description3 = 't r c d', # today reject and cancel
				fullname3 = 't r c f',
				delivery_date3 = now,
				job3 = job1,
				quantity3 = 1,
				price3 = 100,
				delivery_location3 = 'shop',

				description4 = 'tw a d', # this week
				fullname4 = 'tw a f',
				delivery_date4 = twodays,
				job4 = job1,
				quantity4 = 1,
				price4 = 100,
				delivery_location4 = 'shop',

				description5 = 'tw r r d',
				fullname5 = 'tw r r f',
				delivery_date5 = twodays,
				job5 = job1,
				quantity5 = 1,
				price5 = 100,
				delivery_location5 = 'shop',

				description6 = 'tw r c d',
				fullname6 = 'tw r c f',
				delivery_date6 = twodays,
				job6 = job1,
				quantity6 = 1,
				price6 = 100,
				delivery_location6 = 'shop',

				description7 = 'f a d', #future
				fullname7 = 'f a f',
				delivery_date7 = twoweeks,
				job7 = job1,
				quantity7 = 1,
				price7 = 100,
				delivery_location7 = 'shop',

				description8 = 'f r r d',
				fullname8 = 'f r r f',
				delivery_date8 = twoweeks,
				job8 = job1,
				quantity8 = 1,
				price8 = 100,
				delivery_location8 = 'shop',

				description9 = 'f r c d',
				fullname9 = 'f r c f',
				delivery_date9 = twoweeks,
				job9 = job1,
				quantity9 = 1,
				price9 = 100,
				delivery_location9 = 'shop',
				)

			# Job 1 - purchase order items for staff job view RU permissions testing
			self.create_purchase_order(
				description='job 1 - staff job view permissions test desc',
				fullname = 'job 1 - staff job view permissions test fname',
				delivery_date = now,
				job = job1
				)

			# Job 1 - purchase order items for manager CRU permissions test
			self.create_purchase_order(
				description = 'm t a d', # manager today accept description
				fullname = 'm t a f', # today accept fullname
				delivery_date = now,
				job = job1,

				description2 = 'm t r r d', #today reject and reschedule
				fullname2 = 'm t r r f',
				delivery_date2 = now,
				job2 = job1,
				quantity2 = 1,
				price2 = 100,
				delivery_location2 = 'shop',

				description3 = 'm t r c d', # today reject and cancel
				fullname3 = 'm t r c f',
				delivery_date3 = now,
				job3 = job1,
				quantity3 = 1,
				price3 = 100,
				delivery_location3 = 'shop',

				description4 = 'm tw a d', # this week
				fullname4 = 'm tw a f',
				delivery_date4 = twodays,
				job4 = job1,
				quantity4 = 1,
				price4 = 100,
				delivery_location4 = 'shop',

				description5 = 'm tw r r d',
				fullname5 = 'm tw r r f',
				delivery_date5 = twodays,
				job5 = job1,
				quantity5 = 1,
				price5 = 100,
				delivery_location5 = 'shop',

				description6 = 'm tw r c d',
				fullname6 = 'm tw r c f',
				delivery_date6 = twodays,
				job6 = job1,
				quantity6 = 1,
				price6 = 100,
				delivery_location6 = 'shop',

				description7 = 'm f a d', #future
				fullname7 = 'm f a f',
				delivery_date7 = twoweeks,
				job7 = job1,
				quantity7 = 1,
				price7 = 100,
				delivery_location7 = 'shop',

				description8 = 'm f r r d',
				fullname8 = 'm f r r f',
				delivery_date8 = twoweeks,
				job8 = job1,
				quantity8 = 1,
				price8 = 100,
				delivery_location8 = 'shop',

				description9 = 'm f r c d',
				fullname9 = 'm f r c f',
				delivery_date9 = twoweeks,
				job9 = job1,
				quantity9 = 1,
				price9 = 100,
				delivery_location9 = 'shop',
				) 

			# Job 1 - purchase order items for manager job view RU permissions testing
			self.create_purchase_order(
				description='job 1 - manager job view permissions test desc',
				fullname = 'job 1 - manager job view permissions test fname',
				delivery_date = now,
				job = job1
				)




	








	def test_staff_permissions(self):

		with self.settings(NOW = date(year=2017, month=1, day=2)):
			now = settings.NOW

			#-- VISIBILITY --#
	
			# A staff member logs in with the staff password and is redirected to the HOMEPAGE
			self.loginStaff()
			self.wait_for_url(self.live_server_url+reverse('homepage'))
	
			# On the homepage he can see the deliveries and shopping list
			self.wait_until_visible('parent_deliveries_panel')
			self.wait_until_visible('shopping_list_panel')
	
			# He then navigates to the shopping list and finds everything rendering like normal
			self.go_to(reverse('shopping_list'))
			self.wait_until_visible('shopping_list_panel')
			self.assertIn('job 1 shopping list item 1', self.browser.page_source)
			
			# He then navigates to the Jobs page
			self.go_to(reverse('jobs'))
			self.wait_for_url(self.live_server_url+reverse('jobs'))
	
			# He sees only the ongoing jobs tab
			self.wait_until_visible('ongoing_jobs_panel_toggle')
			self.click('ongoing_jobs_panel_toggle')
			self.wait_until_visible('ongoing_jobs_panel')
			# the quotes and completed are not visible, the dropdown menu which houses 'delete job' is not visible
			self.assert_not_visible('completed_jobs_panel_toggle')
			self.assert_not_visible('quote_jobs_panel_toggle')
			self.assert_not_visible('completed_jobs_panel')
			self.assert_not_visible('quote_jobs_panel')
	
	
			# He navigates to an ongoing job view
			self.click('ongoing_jobs_panel_toggle')
			self.wait_until_visible('ongoing_jobs_panel')
			job = Jobs.objects.filter(address='200 Park Avenue').first()
			self.click(f'job_link_{job.pk}')
			# He sees the profile and the site management panel
			self.wait_until_visible('Profile')
			self.wait_until_visible('site_management_panel')
			# In the site management panel he only sees en-route and on-site.
			self.click('en_route_panel_toggle')
			self.wait_until_visible(base_element='site_management_panel', element='en_route_panel')
			self.click('on_site_panel_toggle')
			self.wait_until_visible('on_site_panel')
			# The purchase order tab, notes panel, status drop down menu (on the profile) and schedule of items panel are not visible
			self.assert_not_visible('PO_panel_toggle')
			self.assert_not_visible('PO_panel')
			self.assert_not_visible('notes_panel')
			self.assert_not_visible('status_menu_toggle')
			self.assert_not_visible('status_menu')
			self.assert_not_visible('schedule_of_items_panel')
	
			# He attempts to navigate to the new job form page with the url and finds he is redirected to the home page
			self.go_to(reverse('new_job_form'))
			self.wait_for_url(self.live_server_url+reverse('homepage')) # REFRACT - do I have to put an explicit wait before this check to avoid false positives?
	
			# He attempts to navigate to the purchase order browser and finds the page he is redirected to the home page
			self.go_to(reverse('purchase_orders_browser'))
			self.wait_for_url(self.live_server_url+reverse('homepage')) # REFRACT - do I have to put an explicit wait before this check to avoid false positives?
	
			# He clicks on an item name which links to it's purchase order and finds the page he was on simply reloads # REFRACT - in next version make hyperlinks permission restricted?
			self.go_to(reverse('job', kwargs={'job_id':'200ParkAvenue'}))
			self.wait_until_visible('en_route_panel')
			en_route_item = Items.objects.filter(description='job 1 - purchase order 1 - item 1 description').first()
			self.click(f'po_link_item_{en_route_item.pk}')
			time.sleep(0.5)
			self.wait_for_url(self.live_server_url+reverse('job', kwargs={'job_id':'200ParkAvenue'}))
	
			# He attempts to navigate to the delete job page with the url and finds he is redirected to the home page
			self.go_to(reverse('delete_job'))
			self.wait_for_url(self.live_server_url+reverse('homepage'))
	
		
		#-- CRU --# (deletes is it's own test, the test that staff cannot update items they cannot see the update option for (job status) is covered between the above tests and the unit tests)
	
			# The staff member successfully creates a shopping list item
			# The staff member successfully views the shopping list item in the shopping list - (asserted in the add_shopping_list_method)
			self.add_shopping_list_item('staff added shopping list item', 1, job)
	
			# The staff member successfully 'acquires' the shopping list item (this is both 'updating' a shopping list item and 'creating' an acquired item)
			self.add_acquired_shopping_list_item('staff added acquired shopping list item', 1, job)
	
			# The staff member can successfully view PO items on the home page delivery panel for all three tabs
			self.go_to(reverse('homepage'))
	
			# For all three tabs they can successfully mark them as in-showroom, reject and reschedule them, and reject them
	
			today_item_a = Items.objects.filter(description='t a d').first()
			today_item_r_r = Items.objects.filter(description='t r r d').first()
			today_item_r_c = Items.objects.filter(description='t r c d').first()
	
			this_week_item_a = Items.objects.filter(description='tw a d').first()
			this_week_item_r_r = Items.objects.filter(description='tw r r d').first()
			this_week_item_r_c = Items.objects.filter(description='tw r c d').first()
	
			all_item_a = Items.objects.filter(description='f a d').first()
			all_item_r_r = Items.objects.filter(description='f r r d').first()
			all_item_r_c = Items.objects.filter(description='f r c d').first()
				# today
			self.click('today_deliveries_panel_toggle')
			self.wait_until_visible('today_deliveries_panel')
			self.accept_delivery(today_item_a)
			self.click('today_deliveries_panel_toggle')
			self.wait_until_visible('today_deliveries_panel')
			self.reject_and_reschedule(today_item_r_r)
			self.click('today_deliveries_panel_toggle')
			self.wait_until_visible('today_deliveries_panel')
			self.reject_and_cancel(today_item_r_c)
	
				# this week
			self.click('this_week_deliveries_panel_toggle')
			self.wait_until_visible('this_week_deliveries_panel')
			self.accept_delivery(this_week_item_a)
			self.click('this_week_deliveries_panel_toggle')
			self.wait_until_visible('this_week_deliveries_panel')
			self.reject_and_reschedule(this_week_item_r_r)
			self.click('this_week_deliveries_panel_toggle')
			self.wait_until_visible('this_week_deliveries_panel')
			self.reject_and_cancel(this_week_item_r_c)
	
				# all
			self.click('all_deliveries_panel_toggle')
			self.wait_until_visible('all_deliveries_panel')
			self.accept_delivery(all_item_a)
			self.click('all_deliveries_panel_toggle')
			self.wait_until_visible('all_deliveries_panel')
			self.reject_and_reschedule(all_item_r_r)
			self.click('all_deliveries_panel_toggle')
			self.wait_until_visible('all_deliveries_panel')
			self.reject_and_cancel(all_item_r_c)
	
	
			# The staff member can successfully 1: view PO items in job view en-route
			#									2: mark PO items in job view en-route as on site 
			#  									3: view PO items in job view on-site
			# 									4: view acquired items in job view en-route
			#									5: mark acquired items in job view en-route as on site
			#									6: view acquired items in job view on-site
			# The staff member can successfully view PO items on the job view en-route # REFRACT - this entire mess is a test. make it smoother.
			self.go_to(reverse('job', kwargs={'job_id':'200ParkAvenue'}))
			self.wait_until_visible('site_management_panel')
			self.click('en_route_panel_toggle')
			en_route_item = Items.objects.filter(description='job 1 - staff job view permissions test desc').first()
			self.wait_until_visible(f'en_route_item_{en_route_item.pk}')
			# The staff member can successfully mark PO item on site in the job view en-route panel and then view the PO item in the on-site panel
			self.click(base_element=f'en_route_item_{en_route_item.pk}', element='delivered_button')
			self.wait_for(lambda: self.assertNotIn(f'en_route_item_{en_route_item.pk}', self.browser.page_source))
			self.click('on_site_panel_toggle')
			self.wait_until_visible(f'on_site_item_{en_route_item.pk}')
	
			# The staff member can successfully view acquired items on the job view on-site and en-route panel
				# views acquired item 1 on job-view en-route
			acquired_item = Items.objects.filter(description='job 1 - acquired shopping list item 1 staff').first()
			self.click('en_route_panel_toggle')
			self.wait_for(lambda: self.browser.find_element_by_id(f'en_route_item_{acquired_item.pk}'))
				# marks as on site to then test the on-site panel
			self.click(base_element=f'en_route_item_{acquired_item.pk}', element='delivered_button')
			self.wait_for(lambda: self.assertNotIn(f'en_route_item_{acquired_item.pk}', self.browser.page_source))
				# check on-site panel
			self.click('on_site_panel_toggle')
			self.wait_until_visible(f'on_site_item_{acquired_item.pk}')
	
		
	
	
	
	
		#-- staff deletes --#
		
			#-- notes and admin notes --#
			# this tests the buttons aren't even visible to the staff members, unit tests test they can't delete it # REFRACT - only one shopping list item is needed here as nothing is actually being deleted
		
		
			#--  staff delete Shopping list items --#
		
			# staff member sees a shopping list item he wants to delete in the SHOPPING LIST PAGE
			self.browser.get(self.live_server_url+reverse('shopping_list'))
			self.wait_until_visible('shopping_list_panel')
			shopping_list_page_item_to_delete = Shopping_list_items.objects.filter(description='job 1 shopping list item 1').first()
		
			# staff member clicks the 'del' hyperlink on the far right of the item
			self.click(base_element=f'Shopping_list_items_{shopping_list_page_item_to_delete.pk}', element='delete_shopping_list_item_button')
		
			# The page refreshes and the item remains unchanged
			self.wait_for(lambda: self.assertEqual(self.live_server_url+reverse('shopping_list'), self.browser.current_url))
			self.wait_for(lambda: self.assertIn('job 1 shopping list item 1', self.browser.page_source))
			self.assertIn('job 1 shopping list item 2', self.browser.page_source)
		
		
			# staff member sees a shopping list item he wants to delete in the HOME 
			self.browser.get(self.live_server_url+reverse('homepage'))
			self.wait_until_visible('shopping_list_panel')
			home_page_shopping_list_item_to_delete = Shopping_list_items.objects.filter(description='job 1 shopping list item 2').first()
		
			# staff member clicks the 'del' hyperlink on the far right of the item
			self.click(base_element=f'Shopping_list_items_{home_page_shopping_list_item_to_delete.pk}', element='delete_shopping_list_item_button')
			
			# The page refreshes and the item reloads unchanged
			self.wait_for(lambda: self.assertEqual(self.live_server_url+reverse('homepage'), self.browser.current_url))
			self.wait_for(lambda: self.assertIn('job 1 shopping list item 2', self.browser.page_source))
	
			
		
			#-- Purchase Order items --#
		
			# fts check that staff members are never able to access the delete button, unittests check that they cannot delete it on the backend for integrity's sake
		
			
			
			#-- Items objects with no purchase orders (acquired shopping list items) --#
			
			# staff member sees an acquired shopping list item in the 'en-route' section of a job he wishes to delete
			self.browser.get(self.live_server_url+reverse('job', kwargs={'job_id':'200ParkAvenue'}))
			self.wait_until_visible('site_management_panel')
			self.click('en_route_panel_toggle')
			self.wait_until_visible('en_route_panel')
			acquired_shopping_list_item_to_delete = Items.objects.filter(description='job 1 - acquired shopping list item 1').first()
		
			# Manager clicks the small 'del' hyperlink on the far right of the item
			self.click(base_element=f'en_route_item_{acquired_shopping_list_item_to_delete.pk}', element='delete_item_button') #item.model = acquired, if model == 'acquired' render del button
			# The page refreshes and the item is still there
			self.wait_for(lambda: self.assertEqual(self.live_server_url+reverse('job', kwargs={'job_id':'200ParkAvenue'}), self.browser.current_url))
			self.wait_for(lambda: self.assertIn(f'en_route_item_{acquired_shopping_list_item_to_delete.pk}', self.browser.page_source))
		
			
	
	
	
			#-- Job --#
		
			# fts check that staff members never have access to the form  required to delete this page, unittests will test the backends ability to not delete from staff member
	
	
	#-- manager --#
	
			#-- visiblity --#
	
			# A manager logs in with the manager password and is redirected to the HOMEPAGE
			self.loginManager()
			self.wait_for_url(self.live_server_url+reverse('homepage'))
			# They see everything on the homepage
			for elementid in homepage_elements:
				self.wait_for(lambda: self.browser.find_element_by_id(elementid)) # will this throw an elementNotVisible error? # REFRACT - refract this into a helper method
	
			# He then navigates to the shopping list and finds everything rendering like normal
			self.go_to(reverse('shopping_list'))
			self.wait_for_url(self.live_server_url+reverse('shopping_list'))
			for elementid in shopping_list_elements:
				self.wait_for(lambda: self.browser.find_element_by_id(elementid))
			
			# He navigates to the Jobs page
			self.go_to(reverse('jobs'))
			self.wait_for_url(self.live_server_url+reverse('jobs'))
			# Everything loads as normal except the delete job option
			for elementid in jobs_elements:
				self.wait_for(lambda: self.browser.find_element_by_id(elementid))
			for elementid in jobs_elements_manager_excluded:
				self.wait_for(lambda: self.assertNotIn(f'id="{elementid}"', self.browser.page_source))
			
	
			# He navigates to a job view
			self.go_to(reverse('job', kwargs={'job_id':'200ParkAvenue'}))
			# Everything loads as normal
			for element in job_elements:
				self.wait_for(lambda: self.browser.find_element_by_id(element))
			# He can navigate to the new job form as normal
			self.go_to(reverse('new_job_form'))
			self.wait_for(lambda: self.browser.find_element_by_id('new_job_form'))
	
			# He can navigate to the purchase order browser as normal
			self.go_to(reverse('purchase_orders_browser'))
			self.wait_for(lambda: self.browser.find_element_by_id('purchase_order_number_submit_button'))
	
			# He can navigate to a specific purchase order as normal (the links in the item names remain untouched for this feature, the filter happens when loading the PO)
			self.go_to(reverse('purchase_orders', kwargs={'order_no':1}))
			self.wait_for(lambda: self.browser.find_element_by_id('purchase_order_view_title'))
	
			# He attempts to navigate to the delete job page by typing in the url and finds he is redirected to the homepage
			self.go_to(reverse('homepage'))
			self.wait_until_visible('parent_deliveries_panel')
			self.go_to(reverse('delete_job'))
			self.wait_for_url(self.live_server_url+reverse('homepage'))
	
			#-- CRU --# (deletes is it's own test, the test that staff cannot update items they cannot see the update option for (job status) is covered between the above tests and the unit tests)
	
			# The manager successfully creates a shopping list item
			self.add_shopping_list_item('m perm tests sli', 1, job)
			self.wait_for(lambda: self.assertIn('m perm tests sli', self.browser.page_source))
			# The manager successfully 'acquires' the shopping list item (this is both 'updating' a shopping list item and 'creating' an acquired item)
			self.add_acquired_shopping_list_item('m perm tests asli', 1, job)
	
			# The manager successfully adds a job note
			self.add_job_note('m perm tests jn title', 'm perm tests jn text', job)
			# TODO - the manager successfully edits the job note
			
			# The manager successfully creates a purchase order
			self.create_purchase_order(
				description = 'm test po desc',
				fullname = 'm test po fn',
				delivery_date = now,
				job = job,
				)
			
			today_item_m_a = Items.objects.filter(description='m t a d').first()
			today_item_m_r_r = Items.objects.filter(description='m t r r d').first()
			today_item_m_r_c = Items.objects.filter(description='m t r c d').first()
		
			this_week_item_m_a = Items.objects.filter(description='m tw a d').first()
			this_week_item_m_r_r = Items.objects.filter(description='m tw r r d').first()
			this_week_item_m_r_c = Items.objects.filter(description='m tw r c d').first()
		
			all_item_m_a = Items.objects.filter(description='m f a d').first()
			all_item_m_r_r = Items.objects.filter(description='m f r r d').first()
			all_item_m_r_c = Items.objects.filter(description='m f r c d').first()

			# The manager can successfully view PO items on the home page delivery panel for all three tabs || these are the items that were rescheduled for their original delivery date earlier in the staff CRU tests
			self.go_to(reverse('homepage'))
			self.wait_until_visible('parent_deliveries_panel')
				
			self.click('today_deliveries_panel_toggle')
			self.wait_until_visible('today_deliveries_panel')
			self.wait_until_visible(f'today_delivery_item_{today_item_m_r_r.pk}') # REFRACT - pretty sure this chunk is redundant?
	
			self.click('this_week_deliveries_panel_toggle')
			self.wait_until_visible('this_week_deliveries_panel')
			self.wait_until_visible(f'this_week_delivery_item_{this_week_item_m_r_r.pk}')
	
			self.click('all_deliveries_panel_toggle')
			self.wait_until_visible('all_deliveries_panel')
			self.wait_until_visible(f'all_delivery_item_{all_item_m_r_r.pk}')

			# For all three tabs the manager can successfully mark them as in-showroom, reject and reschedule them, and reject them

				# today
			self.click('today_deliveries_panel_toggle')
			self.wait_until_visible('today_deliveries_panel')
			self.accept_delivery(today_item_m_a)
			self.click('today_deliveries_panel_toggle')
			self.wait_until_visible('today_deliveries_panel')
			self.reject_and_reschedule(today_item_m_r_r)
			self.click('today_deliveries_panel_toggle')
			self.wait_until_visible('today_deliveries_panel')
			self.reject_and_cancel(today_item_m_r_c)
		
				# this week
			self.click('this_week_deliveries_panel_toggle')
			self.wait_until_visible('this_week_deliveries_panel')
			self.accept_delivery(this_week_item_m_a)
			self.click('this_week_deliveries_panel_toggle')
			self.wait_until_visible('this_week_deliveries_panel')
			self.reject_and_reschedule(this_week_item_m_r_r)
			self.click('this_week_deliveries_panel_toggle')
			self.wait_until_visible('this_week_deliveries_panel')
			self.reject_and_cancel(this_week_item_m_r_c)
		
				# all
			self.click('all_deliveries_panel_toggle')
			self.wait_until_visible('all_deliveries_panel')
			self.accept_delivery(all_item_m_a)
			self.click('all_deliveries_panel_toggle')
			self.wait_until_visible('all_deliveries_panel')
			self.reject_and_reschedule(all_item_m_r_r)
			self.click('all_deliveries_panel_toggle')
			self.wait_until_visible('all_deliveries_panel')
			self.reject_and_cancel(all_item_m_r_c)
	
			# The manager can successfully view the schedule of items panels and scheduled items on the job view
			self.go_to(reverse('job', kwargs={'job_id':'200ParkAvenue'}))
				
			self.wait_for(lambda: self.browser.find_element_by_id('schedule_of_items_panel'))
			SI = Scheduled_items.objects.filter(description='job 1 - scheduled item 1 manager').first()
				
			self.browser.find_element_by_id(f'schedule_item_{SI.pk}')
	
			# The manager can successfully 1: view PO items in job view en-route
			#							   2: mark PO items in job view en-route as on site 
			#  							   3: view PO items in job view on-site
			# 							   4: view acquired items in job view en-route
			#							   5: mark acquired items in job view en-route as on site
			#							   6: view acquired items in job view on-site
			# The manager can successfully view PO items on the job view en-route
			self.go_to(reverse('job', kwargs={'job_id':'200ParkAvenue'}))
			self.wait_until_visible('site_management_panel')
			self.click('en_route_panel_toggle')
			en_route_item = Items.objects.filter(description='job 1 - manager job view permissions test desc').first()
			self.wait_until_visible(f'en_route_item_{en_route_item.pk}')
			# The manager can successfully mark PO item on site in the job view en-route panel and then view the PO item in the on-site panel
			self.click(base_element=f'en_route_item_{en_route_item.pk}', element='delivered_button')
			self.wait_for(lambda: self.assertNotIn(f'en_route_item_{en_route_item.pk}', self.browser.page_source))
			self.click('on_site_panel_toggle')
			self.wait_until_visible(f'on_site_item_{en_route_item.pk}')
		
			# The manager can successfully view acquired items on the job view on-site and en-route panel
				# views acquired item 1 on job-view en-route
			acquired_item = Items.objects.filter(description='job 1 - acquired shopping list item 1 manager').first()
			self.click('en_route_panel_toggle')
			self.wait_for(lambda: self.browser.find_element_by_id(f'en_route_item_{acquired_item.pk}'))
				# marks as on site to then test the on-site panel
			self.click(base_element=f'en_route_item_{acquired_item.pk}', element='delivered_button')
			self.wait_for(lambda: self.assertNotIn(f'en_route_item_{acquired_item.pk}', self.browser.page_source))
				# check on-site panel
			self.click('on_site_panel_toggle')
			self.wait_until_visible(f'on_site_item_{acquired_item.pk}')
	
			# The manager can successfully create schedule items
			self.create_schedule_item('testing manager can create schedule item in test', now, 1, Jobs.objects.filter(address="200 Park Avenue").first())
			new_manager_schedule_item = Scheduled_items.objects.filter(description='testing manager can create schedule item in test').first()
			# The manager can successfully edit the dates for the schedule items
				#clicks date button
			self.click(f'schedule_item_{new_manager_schedule_item.pk}_date')
			self.wait_until_visible('date_form_modal')
			update_date_1_day=Select(self.browser.find_element_by_id(f'date_form_modal').find_element_by_id('id_update_date_1_day'))
			update_date_1_day.select_by_value(str(now.day+2))
			update_date_1_year=Select(self.browser.find_element_by_id(f'date_form_modal').find_element_by_id('id_update_date_1_year'))
			update_date_1_year.select_by_value(str(now.year))
			update_date_1_month=Select(self.browser.find_element_by_id(f'date_form_modal').find_element_by_id('id_update_date_1_month'))
			update_date_1_month.select_by_value(str(now.month))
					
					
			self.click(base_element=f'date_form_modal', element='schedule_item_update_button')
	
			self.wait_until_visible('schedule_of_items_panel')
			self.assertIn(f'2017-01-04', self.browser.page_source) # REFRACT - make this dynamically get the date in the correct strf format
	
			# The manager can see all quotes, ongoing and completed jobs
			mReadTest_quote_job = Jobs.objects.filter(address='1 test street').first()
			mReadTest_ongoing_job = Jobs.objects.filter(address='2 test street').first()
			mReadTest_completed_job = Jobs.objects.filter(address='3 test street').first()
			mUpdateTest_job = Jobs.objects.filter(address='4 test street').first()
	
			self.go_to(reverse('jobs'))
			self.wait_until_visible('all_jobs_panel')
	
			self.click('quote_jobs_panel_toggle')
			self.wait_until_visible('quote_jobs_panel_toggle')
			self.wait_until_visible(f'job_link_{mReadTest_quote_job.pk}')
	
				#ongoing
			self.click('ongoing_jobs_panel_toggle')
			self.wait_until_visible('ongoing_jobs_panel')
			self.wait_until_visible(f'job_link_{mReadTest_ongoing_job.pk}')
	
				#complete
			self.click('completed_jobs_panel_toggle')
			self.wait_until_visible('completed_jobs_panel')
			self.wait_until_visible(f'job_link_{mReadTest_completed_job.pk}')
	
			# The manager can update jobs' statuses for each job
			self.go_to(reverse('job', kwargs={'job_id':f'{mUpdateTest_job.job_id}'}))
			self.wait_until_visible('Profile') # is this the id for the profile box?
	
				# Manager clicks on 'ongoing' and finds that after the page has refreshed the box is ultramarine blue
			self.click_menu_button()
			self.click('Ongoing_status_change')
			self.wait_for(lambda: self.assertIn('ULTRAMARINE_BLUE_PROFILE_BOX', self.browser.page_source))		
				
				# Manager clicks on 'completed' and finds that after the page has refreshed the box is a light 
			self.click_menu_button()
			self.click('Completed_status_change')	
			self.wait_for(lambda: self.assertIn('FAINT_BLUE_PROFILE_BOX', self.browser.page_source))	
				
				# Manager clicks on 'quote' (in the dropdown menu) and finds after the page refreshes it is clear
			self.click_menu_button()
			self.click('Quote_status_change')	
			self.wait_for(lambda: self.assertIn('WHITE_PROFILE_BOX', self.browser.page_source))
	
	
			#-- deletes --#	
	
			#-- Notes --#
		
			# The manager sees a note he wants to delete in JOB 1 VIEW (200 Park Avenue)
			self.browser.get(self.live_server_url+reverse('job', kwargs={'job_id':'200ParkAvenue'}))
			self.wait_until_visible('notes_panel')
			job_view_note_to_delete = Notes.objects.filter(Title='job 1 title 1').first()
			job_view_note_to_preserve = Notes.objects.filter(Title='job 1 title 2').first()
		
			# The manager clicks the 'del' hyperlink at the very bottom of the notes text of the note he wants to delete
			self.click(base_element=f'Note_{job_view_note_to_delete.pk}', element='delete_note_button')
			
			# The page refreshes and the note remains
			self.wait_for(lambda: self.assertEqual(self.live_server_url+reverse('job', kwargs={'job_id':'200ParkAvenue'}), self.browser.current_url))
			self.wait_for(lambda: self.assertIn('job 1 title 1', self.browser.page_source)) # REFRACT - waituntilvisible the actual note element
			self.wait_for(lambda: self.assertIn('job 1 title 2', self.browser.page_source))
		
			
			# The manager sees a job note he wants to delete on the HOME PAGE
			self.browser.get(self.live_server_url+reverse('homepage'))
			self.wait_until_visible('notes_panel')
			home_page_note_to_delete = Notes.objects.filter(Title='job 1 title 3').first()
			home_page_note_to_preserve = Notes.objects.filter(Title='job 1 title 4').first()
		
			# The manager clicks the 'all jobs' panel
			self.click('all_notes_panel_toggle')
			self.wait_until_visible('all_notes_panel')
			# The manager clicks the 'del' hyperlink at the very bottom of the notes text
			self.click(base_element=f'Note_{home_page_note_to_delete.pk}', element='delete_note_button')
			
			# The page refreshes and the note remains
			self.wait_for(lambda: self.assertEqual(self.live_server_url+reverse('homepage'), self.browser.current_url))
			self.wait_for(lambda: self.assertIn('job 1 title 3', self.browser.page_source)) # REFRACT - compare element source not whole page
			self.assertIn('job 1 title 4', self.browser.page_source)
		
			
			# The manager clicks to see the admin notes
			self.click('admin_notes_panel_toggle')
			self.wait_until_visible('admin_notes_panel')
			# The manager sees an admin note he wants to delete on the HOME PAGE
			admin_note_to_delete = Notes.objects.filter(Title='admin note 1 title').first()
			admin_note_to_preserve = Notes.objects.filter(Title='admin note 2 title').first()
		
			# The manager clicks the 'del' hyperlink at the very bottom of the notes text
			self.click(base_element=f'Note_{admin_note_to_delete.pk}', element='delete_note_button')
			
			# The page refreshes and the note remains
			self.wait_for(lambda: self.assertEqual(self.live_server_url+reverse('homepage'), self.browser.current_url))
			self.wait_for(lambda: self.assertIn('admin note 1 title', self.browser.page_source)) # REFRACT - compare element source not whole page
			self.assertIn('admin note 2 title', self.browser.page_source)
		
		
		
			#-- Shopping list items --#
		
			# The manager sees a shopping list item he wants to delete in the SHOPPING LIST PAGE
			self.browser.get(self.live_server_url+reverse('shopping_list'))
			self.wait_until_visible('shopping_list_panel')
			shopping_list_page_item_to_delete = Shopping_list_items.objects.filter(description='job 1 shopping list item 1').first()
			shopping_list_page_item_to_preserve = Shopping_list_items.objects.filter(description='job 1 shopping list item 2').first() # REFRACT - is this line being used? check in all other deletions too
		
			# The manager clicks the 'del' hyperlink on the far right of the item
			self.click(base_element=f'Shopping_list_items_{shopping_list_page_item_to_delete.pk}', element='delete_shopping_list_item_button')
		
			# The page refreshes and the item remains
			self.wait_for(lambda: self.assertEqual(self.live_server_url+reverse('shopping_list'), self.browser.current_url))
			self.wait_for(lambda: self.assertIn('job 1 shopping list item 1', self.browser.page_source))
			self.assertIn('job 1 shopping list item 2', self.browser.page_source)
		
		
			# The manager sees a shopping list item he wants to delete in the HOME 
			self.browser.get(self.live_server_url+reverse('homepage'))
			self.wait_until_visible('shopping_list_panel')
			home_page_shopping_list_item_to_delete = Shopping_list_items.objects.filter(description='job 1 shopping list item 2').first()
		
			# The manager clicks the 'del' hyperlink on the far right of the item
			self.click(base_element=f'Shopping_list_items_{home_page_shopping_list_item_to_delete.pk}', element='delete_shopping_list_item_button')
			
			# The page refreshes and the item remains
			self.wait_for(lambda: self.assertEqual(self.live_server_url+reverse('homepage'), self.browser.current_url))
			self.wait_for(lambda: self.assertIn('job 1 shopping list item 2', self.browser.page_source))
		
			
		
			#-- Purchase Order items --#
		
			# The manager sees an item he wants to delete
			self.browser.get(self.live_server_url+reverse('job', kwargs={'job_id':'200ParkAvenue'}))
			self.wait_until_visible('site_management_panel')
			self.click('en_route_panel_toggle')
			self.wait_until_visible('en_route_panel')
			purchase_order_item_to_delete = Items.objects.filter(description = 'job 1 - purchase order 1 - item 1 description').first()
		
			# He clicks on the items name and is redirected to the purchase order view in which the item is contained
			self.click(f'po_link_item_{purchase_order_item_to_delete.pk}')
			self.wait_for(lambda: self.assertEqual(self.live_server_url+reverse('purchase_orders', kwargs={'order_no':purchase_order_item_to_delete.PO.id}), self.browser.current_url))
			purchase_order_url = self.browser.current_url
			# on the far right hand side of the item's row is a 'del' hyperlink. he clicks it, the page refreshes and the item remains on the page
			self.click(base_element=f'PO_item_{purchase_order_item_to_delete.pk}', element='delete_po_item_button')
			self.wait_for(lambda: self.assertEqual(purchase_order_url, self.browser.current_url))
			self.wait_for(lambda: self.assertIn(f'PO_item_{purchase_order_item_to_delete.pk}', self.browser.page_source))
		
			
			
			#-- Items objects with no purchase orders (acquired shopping list items) --#
			
			# The manager sees an acquired shopping list item in the 'en-route' section of a job he wishes to delete
			self.browser.get(self.live_server_url+reverse('job', kwargs={'job_id':'200ParkAvenue'}))
			self.wait_until_visible('site_management_panel')
			self.click('en_route_panel_toggle')
			self.wait_until_visible('en_route_panel')
			acquired_shopping_list_item_to_delete = Items.objects.filter(description='job 1 - acquired shopping list item 1').first()
		
			# The manager clicks the small 'del' hyperlink on the far right of the item
			self.click(base_element=f'en_route_item_{acquired_shopping_list_item_to_delete.pk}', element='delete_item_button')
			# The page refreshes and the item remains
			self.wait_for(lambda: self.assertEqual(self.live_server_url+reverse('job', kwargs={'job_id':'200ParkAvenue'}), self.browser.current_url))
			self.wait_for(lambda: self.assertIn(f'en_route_item_{acquired_shopping_list_item_to_delete.pk}', self.browser.page_source))
	


		#-- Job --#
	
		# manager visibility tests check that manager never even sees the delete job form. Unit tests check the actual delete request would be rejected.
			


#-- superuser --#
	
	# the entire functional test suite for the whole software is run as a superuser.


# ||| REFRACT REFRACT REFRACT - actually write down on paper a flow diagram of what happens in this code, redesign, optimize and rewrite this whole thing to future proof it - REFRACT REFRACT REFRACT |||