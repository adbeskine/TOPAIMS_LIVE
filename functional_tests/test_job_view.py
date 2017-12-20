from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from home.models import Site_info, Items, Shopping_list_items, Scheduled_items
from django.urls import reverse
from datetime import datetime, timedelta, date
import time
from selenium.webdriver.support.ui import Select
from django.conf import settings
NOW = settings.NOW


class JobViewTest(FunctionalTest): 

	#-- HELPER METHODS --#
	def create_job(self):
		#Fills in Tony Stark's details in the new job firm and licks create
		self.browser.get(self.live_server_url + reverse('new_job_form'))
		self.browser.find_element_by_id('Name').send_keys('Tony Stark')
		self.browser.find_element_by_id('Email').send_keys('Tony@StarkIndustries.net')
		self.browser.find_element_by_id('Phone').send_keys('01234567899')
		self.browser.find_element_by_id('Address').send_keys('200 Park Avenue')
		self.browser.find_element_by_id('Note').send_keys("don't ignore JARVIS, he's temperemental and finds it rude")
		ActionChains(self.browser).click(self.browser.find_element_by_id('create')).perform()
		self.wait_for(lambda: self.assertEqual(self.browser.title, 'TopMarks - 200 Park Avenue'))

	def click_menu_button(self):
		ActionChains(self.browser).click(self.browser.find_element_by_id('status_menu_toggle')).perform()

	def add_note(self, title, text):
		self.browser.find_element_by_id('Title_input').send_keys(title)
		self.browser.find_element_by_id('Note_input').send_keys(text)
		ActionChains(self.browser).click(self.browser.find_element_by_id('Add_note')).perform()

	def create_schedule_item(self, name, date1, quantity, date2=None):

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

	def click(self, element, base_element=None):
		if base_element:
			return ActionChains(self.browser).click(self.browser.find_element_by_id(base_element).find_element_by_id(element)).perform()
		else:
			return ActionChains(self.browser).click(self.browser.find_element_by_id(element)).perform()


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



		#-- SETUP AND TEARDOWN --#

	def setUp(self):
		Site_info.objects.create(locked=False, password='thischangesautomaticallyaftereverylock')
		self.browser = webdriver.Chrome()
		self.login()
		self.create_job()


	#-------------------------------------#
		

	




	#-PROFILE-#

	def test_customer_profile_loads_correctly(self):

		# Marek finds on the page a profile section with the customer's name, email, phone and the world quote and sees it is a clear clour
		self.wait_for(lambda: self.browser.find_element_by_id('Profile'))
		Profile = self.browser.find_element_by_id('Profile')
	
		self.assertIn('Name - Tony Stark', Profile.text)
		self.assertIn('Email - Tony@StarkIndustries.net', Profile.text)
		self.assertIn('Phone - 01234567899', Profile.text)
		self.assertIn('Quote', Profile.text)

		self.browser.refresh()

		# POST MVP def test_quote_link_goes_to_correct_cloud_space(self):
			# Marek clicks the word quote and finds he is redirected to a cloud # service #DAVID NEED TO SET THIS UP 	
			# ActionChains(self.browser).click(# self.browser.find_element_by_id('quotelink')).perform()
			# self.fail('POST MVP')

	def test_job_status_change_on_jobview(self):
		
		profile = self.browser.find_element_by_id('Profile')
		status_menu_button = self.browser.find_element_by_id('status_menu_toggle') # REFRACT FURTHER TO DEFINE STATUS_MENU HERE
		
		# Marek clicks the toggle for the dropdown menu and finds three options: quote, ongoing and completed
		self.click_menu_button()
		# test to make sure the menu actually drops down
		
		self.wait_for(lambda: self.assertIn('Quote', self.browser.find_element_by_id('status_menu').text))
		self.wait_for(lambda: self.assertIn('Ongoing', self.browser.find_element_by_id('status_menu').text))
		self.wait_for(lambda: self.assertIn('Complete', self.browser.find_element_by_id('status_menu').text))

		# Marek clicks on 'ongoing' and finds that after the page has refreshed the box is ultramarine blue
		self.click('Ongoing_status_change')
		self.wait_for(lambda: self.assertIn('ULTRAMARINE_BLUE_PROFILE_BOX', self.browser.page_source))		
		
		# Marek clicks on 'completed' and finds that after the page has refreshed the box is a light 
		self.click_menu_button()
		self.click('Completed_status_change')	
		self.wait_for(lambda: self.assertIn('FAINT_BLUE_PROFILE_BOX', self.browser.page_source))	
		
		# Marek clicks on 'quote' (in the dropdown menu) and finds after the page refreshes it is clear
		self.click_menu_button()
		self.click('Quote_status_change')	
		self.wait_for(lambda: self.assertIn('WHITE_PROFILE_BOX', self.browser.page_source))






	#- NOTES -#



	def test_notes_on_jobview(self):

		# Marek sees the note section and decides he wants to add a note
		self.wait_for(lambda: self.browser.find_element_by_id('notes_panel'))
		notes_panel = self.browser.find_element_by_id('notes_panel')
		new_note_form = self.browser.find_element_by_id('new_note_form')

		# Marek fills in the form and clicks 'add note'
		title_1 = 'JARVIS disturbing workers'
		text_1 = "JARVIS keeps pestering the workers with 'suggestions', remind workers to be polite"
		self.add_note(title_1, text_1)

		# The page refreshes and Marek finds his note visible with an alert saying 'note added'
		self.wait_for(lambda: self.assertIn(title_1, self.browser.page_source))
		self.assertIn(text_1, self.browser.page_source)


		# Marek decides to add a second note, he adds the second note, the page refreshes and both notes are visible with the most recent on top
		title_2 = 'JARVIS can read these notes'
		text_2 = "JARVIS reminded our workers that we told them not to ignore him today... has he got nothing more interesting to do?"
		self.add_note(title_2, text_2)

		#	check all the notes appeared
		self.wait_for(lambda: self.assertIn(title_1, self.browser.page_source))
		self.assertIn(text_1, self.browser.page_source)
		self.assertIn(title_2, self.browser.page_source)
		self.assertIn(text_2, self.browser.page_source)

		first_note = self.wait_for(lambda: self.browser.find_element_by_id('Note_4')) #note4 when full test suite run #the first note was made on creation
		second_note = self.browser.find_element_by_id('Note_5') #note5 when full test suite run

		#	check the first note is on the bottom
		self.assertTrue(first_note.location['y'] > second_note.location['y']) # y=0 is the top of the page


	



	

	#- SCHEDULE OF ITEMS -#
	
	

	def test_schedule_of_items(self):


		now = date(month=1, day=10, year=2018)
		current_date = now

		one_month_future_date = current_date.replace(month = current_date.month+1)
		one_month_future_date_minus_one = one_month_future_date.replace(day = one_month_future_date.day-1)
		one_month_future_date_plus_one = one_month_future_date.replace(day = one_month_future_date.day+1)

		current_date_string = str(current_date.strftime('%Y/%d/%m'))
		one_month_future_date_string = str(one_month_future_date.strftime('%Y/%d/%m'))
		one_month_future_date_minus_one_string = str(one_month_future_date_minus_one.strftime('%Y/%d/%m'))
		one_month_future_date_plus_one_string = str(one_month_future_date_plus_one.strftime('%Y/%d/%m'))

		with self.settings(NOW = now):
			self.browser.refresh()

			# Marek sees the schedule of items section and decides to add an item
			self.wait_for(lambda: self.browser.find_element_by_id('schedule_of_items_panel'))
	
			# Marek fills the new item form for one month from the current date and clicks 'add'
			self.create_schedule_item('item 1', date1=one_month_future_date, quantity=1)
			new_item = Scheduled_items.objects.filter(description='item 1').first()
	
			# The page reloads with an alert saying: "item1" successfully scheduled for {future date} "" 
			self.wait_for(lambda: self.assertIn(f'"item 1" successfully scheduled for {one_month_future_date_string}', self.browser.page_source))
			item_1 = self.browser.find_element_by_id('schedule_item_1')
			self.assertIn('item 1', item_1.text)
			self.assertIn('X 1', item_1.text)
			self.assertIn(one_month_future_date_string, item_1.text)
	
			# Marek adds a second item with a final date of one day after the first item
			self.create_schedule_item('item 2', date1=one_month_future_date_minus_one, date2=one_month_future_date_plus_one, quantity=1)
	
			# The page reloads with an alert saying: "item2" successfully scheduled for {one_month_future_date_minus_one} - {one_month_future_date_plus_one} and the new item appearing one above the old item
			self.wait_for(lambda: self.assertIn(f'"item 2" successfully scheduled for {one_month_future_date_minus_one_string} - {one_month_future_date_plus_one_string}', self.browser.page_source))
			item_2 = self.browser.find_element_by_id('schedule_item_2')
			item_1 = self.browser.find_element_by_id('schedule_item_1')
			self.assertTrue(item_2.location['y'] < item_1.location['y']) #remember, y=0 is the top of the screen, furthest away items at the bottom
	
			# Marek decides that actually the first item can wait a few more days so decides to change it's place in the schedule, he clicks on the date, a window appears and he changes the date to make it two days further into the future
	
			self.click('schedule_item_1_date')
			modal = self.wait_for(lambda: self.browser.find_element_by_id('date_form_modal'))

			update_date_1_day=Select(self.browser.find_element_by_id('date_form_modal_1').find_element_by_id('id_update_date_1_day'))
			update_date_1_day.select_by_value(str(one_month_future_date_plus_one.day+14))

			update_date_1_year=Select(self.browser.find_element_by_id('date_form_modal_1').find_element_by_id('id_update_date_1_year'))
			update_date_1_year.select_by_value(str(one_month_future_date_plus_one.year))

			update_date_1_month=Select(self.browser.find_element_by_id('date_form_modal_1').find_element_by_id('id_update_date_1_month'))
			update_date_1_month.select_by_value(str(one_month_future_date_plus_one.month))
				
				
			self.click(base_element='date_form_modal', element='schedule_item_update_button')
	
	
			# The page refreshes and marek sees the changed item appears above the second (more recently scheduled) item and it is no longer highglighted in green
			item_2 = self.wait_for(lambda: self.browser.find_element_by_id('schedule_item_2'))
			item_1 = self.wait_for(lambda: self.browser.find_element_by_id('schedule_item_1'))
			self.wait_for(lambda: self.assertTrue(item_2.location['y'] < item_1.location['y'])) #item one is now the furthest away so item2 should appear on top
	
			# Marek decides to delete item1 altogether, he clicks the item date and sees a tab for delete, he clicks the delete tab
			self.click('schedule_item_1_date')
			modal = self.wait_for(lambda: self.browser.find_element_by_id('date_form_modal'))

			self.click(base_element='date_form_modal', element='delete_tab_toggle')
			# Marek changes his mind, clicks cancel and the modal closes, nothing is deleted
			self.click(base_element='date_form_modal', element='close_modal')
			self.wait_for(lambda: self.browser.find_element_by_id('schedule_item_1'))
	
			# Marek clicks to delete item1 again, this time clicks 'yes' and is redirected back to the job view, with item1 no longer present
			self.click('schedule_item_1_date')
			modal = self.wait_for(lambda: self.browser.find_element_by_id('date_form_modal'))

			self.click(base_element='date_form_modal', element='delete_tab_toggle')
			self.click(base_element='date_form_modal', element='schedule_item_delete')
			self.wait_for(lambda: self.assertNotIn('schedule_item_1', self.browser.page_source))

		#POST MVP
		# after populating the job schedule with another five or six items Marek decides to print the job schedule
	
		# Marek presses the print button and finds that a 'save as' dialogue opens (unit test will test the rest here)



	







#- SITE MANAGEMENT -# NOTE TO SELF see helper methods above

	def test_site_management(self):

		next_week = date.today() + timedelta(days=7)

		self.wait_for(lambda: self.browser.find_element_by_id('site_management_panel'))
		self.create_schedule_item('test itemm 1', date1= NOW+timedelta(days=3), quantity=1)
		self.wait_for(lambda: self.assertIn('test itemm 1', self.browser.page_source))
		new_item = Scheduled_items.objects.filter(description='test itemm 1').first()


		# Marek sees a scheduled item in the scheduled item panel and decides to make a purchase order.
		self.wait_for(lambda: self.browser.find_element_by_id(f'schedule_item_{new_item.pk}'))
		# He clicks on the purchase order button and finds a modal pops up with a purchase order form
		self.click(f'needed_item_Scheduled_items_{new_item.pk}_PO')
		self.wait_for(lambda: self.assertTrue(self.browser.find_element_by_id('purchase_order_modal').is_displayed()))

		# Marek sees that the purchase order has an item pre-filled in with the description, job and quantity
		PO_form = self.browser.find_element_by_id('purchase_order_modal')
		self.assertIn('200 Park Avenue', PO_form.get_attribute("innerHTML"))
		
		PO_item_1_form = self.browser.find_element_by_id('purchase_order_modal').find_element_by_id('item1')
		self.assertIn(f'value="{new_item.quantity}"', PO_item_1_form.get_attribute("innerHTML"))
		self.assertIn('test itemm 1', PO_item_1_form.get_attribute("innerHTML"))
		# Marek fills the rest of the form
		self.slow_type(base_element='purchase_order_modal', element='item_1_fullname_input', string='test item 1 fullname') # god only knows why this was so buggy but was causing a flickering test when done at full speed

		# select delivery location
		delivery_location_1 = Select(self.browser.find_element_by_id('purchase_order_modal').find_element_by_id('item_1_delivery_location_input'))
		delivery_location_1.select_by_value('shop')
		# select delivery date one week from current date
		delivery_date_day=Select(self.browser.find_element_by_id('purchase_order_modal').find_element_by_id('id_item_1_delivery_date_day'))
		delivery_date_day.select_by_value(str(next_week.day))

		delivery_date_year=Select(self.browser.find_element_by_id('purchase_order_modal').find_element_by_id('id_item_1_delivery_date_year'))
		delivery_date_year.select_by_value(str(next_week.year))

		delivery_date_month=Select(self.browser.find_element_by_id('purchase_order_modal').find_element_by_id('id_item_1_delivery_date_month'))
		delivery_date_month.select_by_value(str(next_week.month))


		self.browser.find_element_by_id('purchase_order_modal').find_element_by_id('item_1_price_input').send_keys('100')
		self.browser.find_element_by_id('purchase_order_modal').find_element_by_id('supplier_input').send_keys('Stark Industries')
		self.browser.find_element_by_id('purchase_order_modal').find_element_by_id('supplier_ref_input').send_keys('test item 1 reference')
		
		# Marek clicks create, the purchase order is created and he is redirected back to the job view
		self.click(base_element='purchase_order_modal', element='create_PO')
		self.wait_for(lambda: self.assertEqual(self.browser.current_url, self.live_server_url + reverse('job', kwargs={'job_id':'200ParkAvenue'})))

		new_ordered_item_model_object = Items.objects.filter(fullname='test item 1 fullname').first()
		# Marek sees in the site management panel the item is now in the 'en route' section with the status 'ordered' and showing the expected delivery date
		self.click('en_route_panel_toggle')
		self.wait_for(lambda: self.browser.find_element_by_id('en_route_panel'))

		new_en_route_item = self.browser.find_element_by_id('en_route_panel').find_element_by_id(f'en_route_item_{new_ordered_item_model_object.pk}')

		self.assertIn('test item 1 fullname', new_en_route_item.get_attribute('innerHTML'))
		self.assertIn('status - ORDERED', new_en_route_item.get_attribute('innerHTML'))
		self.assertIn(f'delivery: {new_ordered_item_model_object.delivery_date}', new_en_route_item.get_attribute("innerHTML"))

		# Marek sees another scheduled item and makes it a shopping list item
		self.create_schedule_item('schedule item -> shopping list', quantity=1, date1=NOW)
		self.wait_for(lambda: self.assertIn(' schedule item -&gt; shopping list ', self.browser.page_source)) # -> == -&gt;
		schedule_item_for_shopping_list_model_object = Scheduled_items.objects.filter(description='schedule item -> shopping list').first()
		SI_pk = schedule_item_for_shopping_list_model_object.pk

		# Marek clicks the date button and the modal comes up as before
		self.click(f'schedule_item_{SI_pk}_date')
		self.wait_for(lambda: self.assertTrue(self.browser.find_element_by_id('date_form_modal').is_displayed()))

		# Marek clicks the 'shopping list' tab and sees a standard shopping list form pop up in the modal
		self.click(element=f'shopping_list_form_toggle')
		self.wait_for(lambda: self.assertTrue(self.browser.find_element_by_id('date_form_modal').find_element_by_id(f'shopping_list_form').is_displayed()))

		# Marek sees the shopping list form pre-filled with the item description, quantity and job
		shopping_list_form = self.browser.find_element_by_id('date_form_modal').find_element_by_id(f'shopping_list_form')

		self.assertIn('schedule item -> shopping list', shopping_list_form.get_attribute("innerHTML"))
		self.assertIn('1', shopping_list_form.get_attribute("innerHTML"))
		self.assertIn('200 Park Avenue', shopping_list_form.get_attribute("innerHTML"))

		# Marek sees this is all okay and clicks 'create'
		self.click(base_element='date_form_modal', element='shopping_list_form_submit_button')
		self.wait_for(lambda: self.assertEquals(self.browser.current_url, self.live_server_url + reverse('shopping_list_create', kwargs={'function':'create'})))
		self.wait_for(lambda: self.assertIn('schedule item -&gt; shopping list', self.browser.page_source))
		new_shopping_list_item = Shopping_list_items.objects.filter(description='schedule item -> shopping list').first()
		NSLI_pk = new_shopping_list_item.pk

		# Marek buys the item and clicks 'acquired'
		self.click(base_element=f'Shopping_list_items_{NSLI_pk}', element=f'Shopping_list_items_{NSLI_pk}_acquired_button')
		newly_acquired_item_object = Items.objects.filter(description='schedule item -> shopping list').first()

		# Marek delivers the item to site and clicks 'delivered'
		self.browser.get(self.live_server_url + reverse('job', kwargs={'job_id':'200ParkAvenue'}))
		self.wait_for(lambda: self.click('en_route_panel_toggle'))

		self.click(base_element=f'en_route_item_{newly_acquired_item_object.pk}', element='delivered_button')

		# Marek sees that the item is no longer visible in the 'en-route' panel and is visible in the 'on site' panel
		self.wait_for(lambda: self.click('en_route_panel_toggle'))
		self.wait_for(lambda: self.assertNotIn('id="'+f'en_route_item_{newly_acquired_item_object.pk}"', self.browser.page_source))
		# REFRACT - URGENT - item is no longer visible in 'needed' panel
		self.click('on_site_panel_toggle')
		
		self.wait_for(lambda: self.assertTrue(self.browser.find_element_by_id('on_site_panel').is_displayed()))

		self.assertTrue(self.browser.find_element_by_id('on_site_panel').find_element_by_id(f'on_site_item_{newly_acquired_item_object.pk}').is_displayed())
		
		new_on_site_item = self.browser.find_element_by_id('on_site_panel').find_element_by_id(f'on_site_item_{newly_acquired_item_object.pk}')

		self.assertIn('schedule item -&gt; shopping list', new_on_site_item.get_attribute("innerHTML"))
		self.assertIn('1', new_on_site_item.get_attribute("innerHTML"))

		# Marek now needs to fill out a brand new purchase order so clicks on the P.O tab on site management
		self.browser.refresh()
		self.wait_for(lambda: self.browser.find_element_by_id('site_management_panel'))
		self.click('PO_panel_toggle')
		self.wait_for(lambda: self.assertTrue(self.browser.find_element_by_id('PO_panel').is_displayed()))
		# Marek sees a blank PO
		self.assertTrue(self.browser.find_element_by_id('blank_PO_form').is_displayed())
		# Marek fills it with details for one item to be delivered to site one week from now
		form = self.browser.find_element_by_id('blank_PO_form')

		form.find_element_by_id('supplier_input').send_keys('Stark Industries')
		form.find_element_by_id('supplier_ref_input').send_keys('0002')

		form.find_element_by_id('item_1_description_input').send_keys('PO panel test item description')
		form.find_element_by_id('item_1_fullname_input').send_keys('PO panel test item fullname')
		form.find_element_by_id('item_1_price_input').send_keys('250')
		form_job = Select(form.find_element_by_id('item_1_job_input'))
		form_job.select_by_value('200 Park Avenue')
		form_delivery_location = Select(form.find_element_by_id('item_1_delivery_location_input'))
		form_delivery_location.select_by_value('site')
		time.sleep(0.2)
		form.find_element_by_id('item_1_quantity_input').send_keys('1')

		delivery_date_day=Select(form.find_element_by_id('id_item_1_delivery_date_day'))
		delivery_date_day.select_by_value(str(next_week.day))

		delivery_date_year=Select(form.find_element_by_id('id_item_1_delivery_date_year'))
		delivery_date_year.select_by_value(str(next_week.year))

		delivery_date_month=Select(form.find_element_by_id('id_item_1_delivery_date_month'))
		delivery_date_month.select_by_value(str(next_week.month))

		# Marek clicks to create the purchase order, the page refreshes
		self.click(base_element='PO_panel', element='PO_panel_PO_form_submit_button')
		self.wait_for(lambda: self.assertTrue(self.browser.find_element_by_id('site_management_panel').is_displayed()))

		# Marek checks the en-route panel and sees that the 'PO panel test item fullname' is present
		self.click('en_route_panel_toggle')
		self.wait_for(lambda: self.assertTrue(self.browser.find_element_by_id('en_route_panel').is_displayed()))
		
		self.assertIn('PO panel test item fullname', self.browser.find_element_by_id('en_route_panel').get_attribute("innerHTML"))