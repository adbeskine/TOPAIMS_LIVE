from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from home.models import Site_info, Items, Jobs
from django.urls import reverse
from selenium.webdriver.support.ui import Select
from django.conf import settings
from dateutil.relativedelta import relativedelta
from datetime import date


class HomePageTest(FunctionalTest):

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

	def click(self, element, base_element=None):
		if base_element:
			return ActionChains(self.browser).click(self.browser.find_element_by_id(base_element).find_element_by_id(element)).perform()
		else:
			return ActionChains(self.browser).click(self.browser.find_element_by_id(element)).perform()

	def click_element(self, element):
		return ActionChains(self.browser).click(element).perform()

	def wait_until_visible(self, element, base_element=None):
		if base_element:
			return self.wait_for(lambda: self.assertTrue(self.browser.find_element_by_id(base_element).find_element_by_id(element).is_displayed()))
		else:
			return self.wait_for(lambda: self.assertTrue(self.browser.find_element_by_id(element).is_displayed()))

	def create_purchase_order_item(self, description, fullname, delivery_date, job, supplier='Stark Industries', supplier_ref='123', quantity=1, price=1, delivery_location='shop'):
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

		# Marek clicks to create the purchase order, the page refreshes
		self.click(base_element='PO_panel', element='PO_panel_PO_form_submit_button')
		self.wait_for(lambda: self.assertTrue(self.browser.find_element_by_id('site_management_panel').is_displayed()))
		self.browser.get(self.live_server_url+reverse('homepage'))
		return self.wait_until_visible('parent_deliveries_panel') #rewrite this to manually fill in a form somewhere

	def create_custom_job(self, name, email, phone, address, note, status): # REFRACT make this actually create db objects instead of manually typing everything
		self.browser.get(self.live_server_url + reverse('new_job_form'))
		self.browser.find_element_by_id('Name').send_keys(name)
		self.browser.find_element_by_id('Email').send_keys(email)
		self.browser.find_element_by_id('Phone').send_keys(phone)
		self.browser.find_element_by_id('Address').send_keys(address)
		self.browser.find_element_by_id('Note').send_keys(note)
		ActionChains(self.browser).click(self.browser.find_element_by_id('create')).perform()
		self.wait_for(lambda: self.assertEqual(self.browser.title, f'TopMarks - {address}'))

	def add_note(self, title, text):
		self.browser.find_element_by_id('Title_input').send_keys(title)
		self.browser.find_element_by_id('Note_input').send_keys(text)
		ActionChains(self.browser).click(self.browser.find_element_by_id('Add_note')).perform()

		"""the arguments that NEED to be specified are 'description', 'fullname' and 'delivery_date'.
		Everything else has overridable but default values. This posts valid post data to url:purchase_order"""


	#-- SETUP AND TEARDOWN --#

	def setUp(self):
		with self.settings(NOW = date(year=2017, month=1, day=2)): # stops the tests screwing up, make sure now is a monday (so now + a few days == later THIS week)
			now = settings.NOW
			Site_info.objects.create(locked=False, password='thischangesautomaticallyaftereverylock')
			self.browser = webdriver.Chrome()
			self.login()
			self.create_job()
			job = Jobs.objects.filter(address='200 Park Avenue').first()
			self.create_purchase_order_item('today 1', 'today fname 1', now, job)
			self.create_purchase_order_item('today 2', 'today fname 2', now, job)
			self.create_purchase_order_item('today 3', 'today fname 3', now, job)
			self.create_purchase_order_item('thisweek 1', 'thisweek fname 1', now+relativedelta(days=2), job)
			self.create_purchase_order_item('nextweek 1', 'nextweek fname 1', now+relativedelta(weeks=2), job)

	#------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
	#------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
	#------------------------------------------------------------------------------------------------------------------------------------------------------------------------#



	def test_home_page_deliveries_panel(self):

		with self.settings(NOW = date(year=2017, month=1, day=2)): # stops the tests screwing up, make sure now is a monday (so now + a few days == later THIS week)
			#- DATA SETUP --#
			now = settings.NOW

			today_1_object = Items.objects.filter(description='today 1').first()
			today_2_object = Items.objects.filter(description='today 2').first()
			today_3_object = Items.objects.filter(description='today 3').first()
			this_week_1_object = Items.objects.filter(description='thisweek 1').first()
			next_week_1_object = Items.objects.filter(description='nextweek 1').first()
	
		#- DELIVERIES -#
			today_deliveries_panel = self.browser.find_element_by_id('today_deliveries_panel')
			this_week_deliveries_panel = self.browser.find_element_by_id('parent_deliveries_panel').find_element_by_id('this_week_deliveries_panel')
			all_deliveries_panel = self.browser.find_element_by_id('parent_deliveries_panel').find_element_by_id('all_deliveries_panel')

			today_deliveries_panel_toggle = self.browser.find_element_by_id('parent_deliveries_panel').find_element_by_id('today_deliveries_panel_toggle')
			this_week_deliveries_panel_toggle = self.browser.find_element_by_id('parent_deliveries_panel').find_element_by_id('this_week_deliveries_panel_toggle')
			all_deliveries_panel_toggle = self.browser.find_element_by_id('parent_deliveries_panel').find_element_by_id('all_deliveries_panel_toggle')
			# When Marek enters the home page he sees all of the the day's deliveries. By default it displays all the deliveries being expected for 'today'
			self.browser.get(self.live_server_url+reverse('homepage'))
			
			self.wait_until_visible(base_element='parent_deliveries_panel', element='today_deliveries_panel')
			self.click('today_deliveries_panel_toggle')
			today_deliveries_panel = self.browser.find_element_by_id('today_deliveries_panel')
	
			self.assertIn('today fname 1', today_deliveries_panel.get_attribute("innerHTML"))
			self.assertIn('today fname 2', today_deliveries_panel.get_attribute('innerHTML'))
			self.assertIn('today fname 3', today_deliveries_panel.get_attribute('innerHTML'))
	
			# Marek sees three tabs on the deliveries panel: 'today', 'this week', 'all'
			self.wait_until_visible(base_element='parent_deliveries_panel', element='today_deliveries_panel_toggle')
			today_deliveries_panel_toggle = self.browser.find_element_by_id('parent_deliveries_panel').find_element_by_id('today_deliveries_panel_toggle')
			self.wait_until_visible(base_element='parent_deliveries_panel', element='this_week_deliveries_panel_toggle')
			this_week_deliveries_panel_toggle = self.browser.find_element_by_id('parent_deliveries_panel').find_element_by_id('this_week_deliveries_panel_toggle')
			self.wait_until_visible(base_element='parent_deliveries_panel', element='all_deliveries_panel_toggle')
			all_deliveries_panel_toggle = self.browser.find_element_by_id('parent_deliveries_panel').find_element_by_id('all_deliveries_panel_toggle')
	
			# Marek clicks 'this week' and all the deliveries for this week are shown
			self.click_element(this_week_deliveries_panel_toggle)
			self.wait_until_visible(base_element='parent_deliveries_panel', element='this_week_deliveries_panel')
			this_week_deliveries_panel = self.browser.find_element_by_id('parent_deliveries_panel').find_element_by_id('this_week_deliveries_panel')
	
			self.assertIn('thisweek fname 1', this_week_deliveries_panel.get_attribute('innerHTML'))
	
	
			# Marek clicks 'all' and the page refreshes to show every delivery in an unlimited time window
			self.click_element(all_deliveries_panel_toggle)
			self.wait_until_visible(base_element='parent_deliveries_panel', element='all_deliveries_panel')
			all_deliveries_panel = self.browser.find_element_by_id('parent_deliveries_panel').find_element_by_id('all_deliveries_panel')
	
			self.assertIn('nextweek fname 1', all_deliveries_panel.get_attribute('innerHTML'))
			
			# Marek clicks 'today' and the page reverts back to the original view
			self.click_element(today_deliveries_panel_toggle)
			self.wait_until_visible(base_element='parent_deliveries_panel', element='today_deliveries_panel')
	
			# 'today fname 1' arrives and Marek sees it is all correct so clicks the 'accept delivery' button
			self.click(base_element='today_deliveries_panel', element=f'accept_delivery_button_{today_1_object.pk}')
	
			# The page refreshes, the item disappears from the view || SYNCHRONISATION
			today_deliveries_panel = self.browser.find_element_by_id('today_deliveries_panel')

			self.wait_for(lambda: self.assertNotIn('today fname 1', today_deliveries_panel.get_attribute("innerHTML")))
			# The item appears as status 'IN SHOWROOM' in it's en-route panel
			self.browser.get(self.live_server_url+reverse('job', kwargs={'job_id':'200ParkAvenue'}))
			self.wait_until_visible('site_management_panel')
			self.click(base_element='site_management_panel', element='en_route_panel_toggle')
			en_route_panel = self.browser.find_element_by_id('site_management_panel').find_element_by_id('en_route_panel')
	
			self.wait_for(lambda: self.assertIn('today fname 1 </a>| status - IN SHOWROOM', en_route_panel.get_attribute('innerHTML'))) # the closing anchor tag is always there because of the potential PO hyperlink
	
			
	
			# 'today fname 2' arrives but this time Marek sees the item is damaged, he clicks the 'reject delivery' button, a modal pops up with the item rejection form.
			self.browser.get(self.live_server_url+reverse('homepage'))
			self.wait_until_visible('parent_deliveries_panel')
			self.click(base_element='today_deliveries_panel', element=f'reject_delivery_button_{today_2_object.pk}')
			self.wait_until_visible(f'delivery_rejection_modal_{today_2_object.pk}')
			delivery_rejection_form = self.browser.find_element_by_id(f'delivery_rejection_modal_{today_2_object.pk}').find_element_by_id('delivery_rejection_form')
			
			# Marek reschedules for another delivery, adds a note and clicks submit, he finds he is redirected to the home page with an alert saying '{{ item description }} rejected'
			delivery_rejection_form.find_element_by_id('id_note').send_keys('item is damaged')
			reschedule_date_year = Select(delivery_rejection_form.find_element_by_id('id_reschedule_date_year'))
			reschedule_date_year.select_by_value(str(now.year))
			reschedule_date_day = Select(delivery_rejection_form.find_element_by_id('id_reschedule_date_day'))
			reschedule_date_day.select_by_value(str(now.day+2))
			reschedule_date_month = Select(delivery_rejection_form.find_element_by_id('id_reschedule_date_month'))
			reschedule_date_month.select_by_value(str(now.month))
			self.click(base_element=f'delivery_rejection_modal_{today_2_object.pk}', element='reject_delivery_form_submit')

			self.wait_for(lambda: self.assertIn('today 2 rejected', self.browser.page_source))
			today_2_object = Items.objects.filter(description='today 2').first()
			# In the homepage Marek checks the 'this week' tab on the delivery items and sees the item rescheduled for the selected date
			this_week_deliveries_panel_toggle = self.browser.find_element_by_id('parent_deliveries_panel').find_element_by_id('this_week_deliveries_panel_toggle')
			self.click_element(this_week_deliveries_panel_toggle)
			this_week_deliveries_panel = self.browser.find_element_by_id('parent_deliveries_panel').find_element_by_id('this_week_deliveries_panel')
			self.wait_for(lambda: self.assertIn('today fname 2', this_week_deliveries_panel.get_attribute('innerHTML'))) # TODO show delivery date 
			
			# Marek checks the job view and sees the item as 'en-route' in the delivery panel
			self.browser.get(self.live_server_url+reverse('job', kwargs={'job_id':'200ParkAvenue'}))
			self.wait_until_visible('site_management_panel')
			self.click(base_element='site_management_panel', element='en_route_panel_toggle')
			en_route_panel = self.browser.find_element_by_id('site_management_panel').find_element_by_id('en_route_panel')

			en_route_panel_stripped = ''.join(letter for letter in en_route_panel.get_attribute("innerHTML") if letter.isalnum())
			string = f'today fname 2 </a>| status - ORDERED | delivery: {today_2_object.delivery_date}' # the closing anchor tag is always there because of the potential PO hyperlink
			stripped_string = ''.join(letter for letter in string if letter.isalnum())
	
			self.wait_for(lambda: self.assertIn(stripped_string, en_route_panel_stripped)) # may render in the FT differently to the browser, edit as needed
	
			# Marek also sees the rejection note on the top of the notes with auto-generated title: 'TODAY 2 REJECTED' (description, NOT fullname)
			notes_panel = self.browser.find_element_by_id('notes_panel')
	
			self.wait_for(lambda: self.assertIn('ITEM REJECTED - today 2', notes_panel.get_attribute('innerHTML')))
			self.wait_for(lambda: self.assertIn(f'item is damaged || rescheduled for delivery on {today_2_object.delivery_date}', notes_panel.get_attribute('innerHTML'))) # edit to match browser
	
			
			self.browser.get(self.live_server_url+reverse('homepage'))
			self.wait_until_visible('parent_deliveries_panel')	
			# 'today fname 3' arrives and Marek must reject delivery, this time he does not reschedule
			self.click(base_element='parent_deliveries_panel', element='today_deliveries_panel_toggle')
			self.click(base_element='today_deliveries_panel', element=f'reject_delivery_button_{today_3_object.pk}')
			
			self.wait_until_visible(f'delivery_rejection_modal_{today_3_object.pk}')
			delivery_rejection_form = self.browser.find_element_by_id(f'delivery_rejection_modal_{today_3_object.pk}').find_element_by_id('delivery_rejection_form')
			
			# Marek fills the rejection with a form and leaves the date blank because it is not being rescheduled
			delivery_rejection_form.find_element_by_id('id_note').send_keys('item is damaged')
			self.click(base_element=f'delivery_rejection_modal_{today_3_object.pk}', element='reject_delivery_form_submit')

			# because the item has not been rescheduled, Marek does not see it in the delivery panel at all
			self.wait_until_visible('parent_deliveries_panel') #page reloads from form submission
			today_deliveries_panel = self.browser.find_element_by_id('today_deliveries_panel')
			this_week_deliveries_panel = self.browser.find_element_by_id('parent_deliveries_panel').find_element_by_id('this_week_deliveries_panel')
			all_deliveries_panel = self.browser.find_element_by_id('parent_deliveries_panel').find_element_by_id('all_deliveries_panel')
			today_deliveries_panel_toggle = self.browser.find_element_by_id('parent_deliveries_panel').find_element_by_id('today_deliveries_panel_toggle')
			this_week_deliveries_panel_toggle = self.browser.find_element_by_id('parent_deliveries_panel').find_element_by_id('this_week_deliveries_panel_toggle')
			all_deliveries_panel_toggle = self.browser.find_element_by_id('parent_deliveries_panel').find_element_by_id('all_deliveries_panel_toggle')
	
			self.assertNotIn('today fname 3', today_deliveries_panel.get_attribute("innerHTML"))
	
			self.click_element(this_week_deliveries_panel_toggle)
			self.wait_until_visible('this_week_deliveries_panel')
			self.assertNotIn('today fname 3', this_week_deliveries_panel.get_attribute("innerHTML"))
	
			self.click_element(all_deliveries_panel_toggle)
			self.wait_until_visible('all_deliveries_panel')
			self.assertNotIn('today fname 3', all_deliveries_panel.get_attribute("innerHTML"))
	
			# Marek goes to the job view and sees a note is left in the job view, the item in the 'needed items' column with an ammendment saying 'delivery rejected', he does NOT see the item in the en-route section
			self.browser.get(self.live_server_url+reverse('job', kwargs={'job_id':'200ParkAvenue'}))
			self.wait_until_visible('site_management_panel')
	
			notes_panel=self.browser.find_element_by_id('notes_panel')
	
			self.wait_for(lambda: self.assertIn('ITEM REJECTED - today 3', notes_panel.get_attribute('innerHTML')))
			self.wait_for(lambda: self.assertIn('item is damaged || NOT RESCHEDULED', notes_panel.get_attribute('innerHTML'))) # edit to match browser
	
			"""site_management_panel = self.browser.find_element_by_id('site_management_panel')
			needed_item_today_3 = site_management_panel.find_element_by_id('ne') """
	
	#- Shopping List -#
			self.browser.get(self.live_server_url+reverse('homepage'))
			# Marek now checks the shopping list, he can see the items displaying in reverse chronological order
			self.wait_until_visible('shopping_list_panel')
			shopping_list_panel = self.browser.find_element_by_id('shopping_list_panel')
			# Marek decides to add a new item to the shopping list, he fills in the form and hits submit, the page refreshes and the new item is at the top
			self.browser.find_element_by_id('new_shopping_list_item_form').find_element_by_id('shopping_list_description_input').send_keys('homepage shopping list item 1')
			self.browser.find_element_by_id('new_shopping_list_item_form').find_element_by_id('shopping_list_quantity_input').send_keys('1')
			shopping_list_job_choice = Select(self.browser.find_element_by_id('new_shopping_list_item_form').find_element_by_id('shopping_list_job_input'))
			shopping_list_job_choice.select_by_value('200 Park Avenue') # may have to change the base elements here to the shopping list panel (not the form)
			self.click(base_element='new_shopping_list_item_form', element='shopping_list_form_submit_button')
			
			self.wait_until_visible('parent_deliveries_panel')
			shopping_list_panel = self.browser.find_element_by_id('shopping_list_panel')

			self.wait_for(lambda: self.assertIn('homepage shopping list item 1', shopping_list_panel.get_attribute("innerHTML")))
	
	
	# POST MVP - Marek then looks at an item on the shopping list and decides to make a purchase order from it
	# POST MVP - Marek finds the form pre filled with the item's description, quantity and job, Marek clicks create and finds he is redirected back to the home page || VALIDATION
	
	# POST MVP - Marek sees the item no longer on the shopping list
	
	#- Notes -#
	
			# Marek starts two more jobs then goes back to the home page
			self.create_custom_job(name='Nick Fury', email='NF@SHIELD.com', phone='01234567898', address='59th Madison Avenue', status='completed', note="Nick Fury's job")
			self.create_custom_job(name='Matt Murdock', email='mmurdoch@NelsonandMurdock.org', phone='01234567898', address='Hells Kitchen', status='ongoing', note="Matt Murdock's job")
			# Marek navigates back to the homepage
			self.browser.get(self.live_server_url+reverse('homepage'))
			self.wait_until_visible('parent_deliveries_panel')

			# Now Marek is looking at the notes section and sees two tabs, 'admin' and 'all jobs'
			self.wait_until_visible('notes_panel')
			notes_panel = self.browser.find_element_by_id('notes_panel')
			admin_notes_panel_toggle = notes_panel.find_element_by_id('admin_notes_panel_toggle')
			all_notes_panel_toggle = notes_panel.find_element_by_id('all_notes_panel_toggle')
			
			# Marek clicks 'all', and he can now see all the notes from every job (but not the admin notes) in reverse chronological order
			self.click_element(all_notes_panel_toggle)
			self.wait_until_visible('all_notes_panel')
			all_notes_panel = self.browser.find_element_by_id('all_notes_panel')
			
			self.assertIn("Nick Fury's job", all_notes_panel.get_attribute("innerHTML"))
			self.assertIn("Matt Murdock's job", all_notes_panel.get_attribute("innerHTML"))
	
			# Marek clicks 'admin' again and finds the page reverts to the admin notes
			self.click_element(admin_notes_panel_toggle)
			self.wait_until_visible('admin_notes_panel')
			admin_notes_panel = self.browser.find_element_by_id('admin_notes_panel')
	
			self.assertNotIn("Nick Fury's job", admin_notes_panel.get_attribute("innerHTML"))
			self.assertNotIn("Matt Murdock's job", admin_notes_panel.get_attribute("innerHTML"))
			
			# Marek then decides to add a new note, he fills in the form and clicks add, the page refreshes with the alert 'note successfully added' and the new note appears in 'admin' on the top || FORM VALIDATION
			self.add_note(title='test admin note TITLE', text='test admin note TEXT')
			self.wait_until_visible('parent_deliveries_panel')

			admin_notes_panel = self.browser.find_element_by_id('admin_notes_panel')
			self.wait_for(lambda: self.assertIn('test admin note TITLE', admin_notes_panel.get_attribute("innerHTML")))
			self.wait_for(lambda: self.assertIn('test admin note TEXT', admin_notes_panel.get_attribute("innerHTML")))
	
	
			#- Purchase Order -#
			# (the code for this and purchase order form page are taken from the same place see there for more detailed testing)
			
			purchase_order_panel = self.browser.find_element_by_id('PO_panel')
			form = self.browser.find_element_by_id('blank_PO_form')
			# Marek needs to fill out a new purchase order
			form.find_element_by_id('supplier_input').send_keys('Stark Industries')
			form.find_element_by_id('supplier_ref_input').send_keys('0003')
			
			# Marek fills out item A to be delivered to the shop for job A for the same day
			
			form.find_element_by_id('item_1_description_input').send_keys('item A description')
			form.find_element_by_id('item_1_fullname_input').send_keys('item A fullname')
			form.find_element_by_id('item_1_price_input').send_keys('250')
			form_job = Select(form.find_element_by_id('item_1_job_input'))
			form_job.select_by_value('200 Park Avenue')
			form_delivery_location = Select(form.find_element_by_id('item_1_delivery_location_input'))
			form_delivery_location.select_by_value('shop')
			form.find_element_by_id('item_1_quantity_input').send_keys('1')
			delivery_date_day=Select(form.find_element_by_id('id_item_1_delivery_date_day'))
			delivery_date_day.select_by_value(str(now.day))
	
			delivery_date_year=Select(form.find_element_by_id('id_item_1_delivery_date_year'))
			delivery_date_year.select_by_value(str(now.year))
	
			delivery_date_month=Select(form.find_element_by_id('id_item_1_delivery_date_month'))
			delivery_date_month.select_by_value(str(now.month))
			
			# Marek fills out item B to be delivered to site for job B
			
			form.find_element_by_id('item_2_description_input').send_keys('item B description')
			form.find_element_by_id('item_2_fullname_input').send_keys('item B fullname')
			form.find_element_by_id('item_2_price_input').send_keys('250')
			form_job = Select(form.find_element_by_id('item_2_job_input'))
			form_job.select_by_value('Hells Kitchen')
			form_delivery_location = Select(form.find_element_by_id('item_2_delivery_location_input'))
			form_delivery_location.select_by_value('site')
			form.find_element_by_id('item_2_quantity_input').send_keys('1')
			delivery_date_day=Select(form.find_element_by_id('id_item_2_delivery_date_day'))
			delivery_date_day.select_by_value(str(now.day))
	
			delivery_date_year=Select(form.find_element_by_id('id_item_2_delivery_date_year'))
			delivery_date_year.select_by_value(str(now.year))
	
			delivery_date_month=Select(form.find_element_by_id('id_item_2_delivery_date_month'))
			delivery_date_month.select_by_value(str(now.month))
			
			# Marek fills out item C to be delivered to the shop for job A for later on in the week
			later = now+relativedelta(days=2)
	
			form.find_element_by_id('item_3_description_input').send_keys('item C description')
			form.find_element_by_id('item_3_fullname_input').send_keys('item C fullname')
			form.find_element_by_id('item_3_price_input').send_keys('250')
			form_job = Select(form.find_element_by_id('item_3_job_input'))
			form_job.select_by_value('200 Park Avenue')
			form_delivery_location = Select(form.find_element_by_id('item_3_delivery_location_input'))
			form_delivery_location.select_by_value('shop')
			form.find_element_by_id('item_3_quantity_input').send_keys('1')
			delivery_date_day=Select(form.find_element_by_id('id_item_3_delivery_date_day'))
			delivery_date_day.select_by_value(str(later.day))
	
			delivery_date_year=Select(form.find_element_by_id('id_item_3_delivery_date_year'))
			delivery_date_year.select_by_value(str(later.year))
	
			delivery_date_month=Select(form.find_element_by_id('id_item_3_delivery_date_month'))
			delivery_date_month.select_by_value(str(later.month))
	
			# Marek fills out item D to be delivered to the shop for job A two weeks time then clicks create
	
			two_weeks_later = now+relativedelta(weeks=2)
	
			form.find_element_by_id('item_4_description_input').send_keys('item D description')
			form.find_element_by_id('item_4_fullname_input').send_keys('item D fullname')
			form.find_element_by_id('item_4_price_input').send_keys('250')
			form_job = Select(form.find_element_by_id('item_4_job_input'))
			form_job.select_by_value('200 Park Avenue')
			form_delivery_location = Select(form.find_element_by_id('item_4_delivery_location_input'))
			form_delivery_location.select_by_value('shop')
			form.find_element_by_id('item_4_quantity_input').send_keys('1')
			delivery_date_day=Select(form.find_element_by_id('id_item_4_delivery_date_day'))
			delivery_date_day.select_by_value(str(two_weeks_later.day))
	
			delivery_date_year=Select(form.find_element_by_id('id_item_4_delivery_date_year'))
			delivery_date_year.select_by_value(str(two_weeks_later.year))
	
			delivery_date_month=Select(form.find_element_by_id('id_item_4_delivery_date_month'))
			delivery_date_month.select_by_value(str(two_weeks_later.month))
	
			self.click(base_element='PO_panel', element='PO_panel_PO_form_submit_button')
	
			# As the page reloads Marek sees item A appearing in today's deliveries list (note: item b wont appear anywhere here because it's being delivered to site)
			self.wait_until_visible('parent_deliveries_panel')
			today_deliveries_panel = self.browser.find_element_by_id('today_deliveries_panel')
			this_week_deliveries_panel = self.browser.find_element_by_id('parent_deliveries_panel').find_element_by_id('this_week_deliveries_panel')
			all_deliveries_panel = self.browser.find_element_by_id('parent_deliveries_panel').find_element_by_id('all_deliveries_panel')

			today_deliveries_panel_toggle = self.browser.find_element_by_id('parent_deliveries_panel').find_element_by_id('today_deliveries_panel_toggle')
			this_week_deliveries_panel_toggle = self.browser.find_element_by_id('parent_deliveries_panel').find_element_by_id('this_week_deliveries_panel_toggle')
			all_deliveries_panel_toggle = self.browser.find_element_by_id('parent_deliveries_panel').find_element_by_id('all_deliveries_panel_toggle')
	
			self.assertIn('item A fullname', today_deliveries_panel.get_attribute("innerHTML"))
			self.assertNotIn('item B fullname', today_deliveries_panel.get_attribute("innerHTML"))
	
			# Marek looks at the 'this week' section of the deliveries and sees item C appearing in the deliveries list
			self.click_element(this_week_deliveries_panel_toggle)
			self.wait_until_visible('this_week_deliveries_panel')
	
			self.assertIn('item C fullname', this_week_deliveries_panel.get_attribute("innerHTML"))
	
			# Marek then looks at the 'all' section of the deliveries and sees item D appearing in the deliveries list
			self.click_element(all_deliveries_panel_toggle)
			self.wait_until_visible('all_deliveries_panel')
	
			self.assertIn('item D fullname', all_deliveries_panel.get_attribute("innerHTML"))