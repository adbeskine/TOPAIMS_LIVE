from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from django.urls import reverse
from selenium.webdriver.support.ui import Select
from django.conf import settings
from dateutil.relativedelta import relativedelta
from datetime import date

from _Auth.models import Site_info
from Item_Flow.models import Items, Purchase_orders
from Jobs.models import Jobs


class PurchaseOrderViewTest(FunctionalTest):

	# -- DESCRIPTION --#
	""" this test finds every instance in the software where an Item object's name appears (aside from in the PO view) and when you click it it links to the purchase order
		WHENEVER a new instance of an item's fullname appears add it to this test 
	"""

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

	def create_purchase_order_item(self, description, fullname, delivery_date, job, supplier='Stark Industries', supplier_ref='123', quantity=1, price=10, delivery_location='shop'):
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

		self.click(base_element='PO_panel', element='PO_panel_PO_form_submit_button')
		self.wait_for(lambda: self.assertTrue(self.browser.find_element_by_id('site_management_panel').is_displayed()))

	def wait_until_visible(self, element, base_element=None):
		# element = the element id tag
		if base_element:
			return self.wait_for(lambda: self.assertTrue(self.browser.find_element_by_id(base_element).find_element_by_id(element).is_displayed()))
		else:
			return self.wait_for(lambda: self.assertTrue(self.browser.find_element_by_id(element).is_displayed()))

	#-- SETUP AND TEARDOWN --#

	def setUp(self):
		now = settings.NOW
		Site_info.objects.create(locked=False, password='thischangesautomaticallyaftereverylock')
		self.browser = webdriver.Chrome()
		self.login()
		self.create_job()
		
	#---------------------------------------------------#

	def test_PO_view(self):
		with self.settings(NOW = date(year=2017, month=1, day=2)): # stops the tests screwing up, make sure now is a monday (so now + a few days == later THIS week)
			now = settings.NOW
			# Marek makes three purchase orders for Tony Stark
			job = Jobs.objects.filter(address='200 Park Avenue').first()
			self.create_purchase_order_item('today 1', 'today fname 1', now, job, supplier_ref='1')
			today_1_order_no = Purchase_orders.objects.filter(supplier_ref='1').first().id
			today_1_item = Items.objects.filter(description='today 1').first()
	
			self.create_purchase_order_item('today 2', 'today fname 2', now+relativedelta(days=2), job, supplier_ref='2')
			today_2_order_no = Purchase_orders.objects.filter(supplier_ref='2').first().id
			today_2_item = Items.objects.filter(description='today 2').first()
	
			self.create_purchase_order_item('today 3', 'today fname 3', now, job, supplier_ref='3')
			today_3_order_no = Purchase_orders.objects.filter(supplier_ref='3').first().id
			today_3_item = Items.objects.filter(description='today 3').first()
	
			self.create_purchase_order_item('today 4', 'today fname 4', now+relativedelta(days=20), job, supplier_ref='4')
			today_4_order_no = Purchase_orders.objects.filter(supplier_ref='4').first().id
			today_4_item = Items.objects.filter(description='today 4').first() # REFRACT the only reason this is here is because 
			# there needs to be an item in the 'all deliveries' section and the third item gets marked as delivered before the tests run on the homepage.
			# refract to get change the order of the tests so the test for the 'all deliveries' and the 'on site' panel gets run on today 3 and eliminating the need
			# for today4
	
			# Marek navigates to the purchase order view and sees a dropdown menu to browse the purchase orders.
			self.browser.get(self.live_server_url+reverse('purchase_orders_browser'))
			self.wait_until_visible('purchase_order_number_input')
			
			# He clicks purchase order 4001 and clicks 'Go'. He is redirected to the purchase order view.
			purchase_order_choice = Select(self.browser.find_element_by_id('purchase_order_number_input'))
			purchase_order_choice.select_by_value(str(today_1_order_no))
			self.click('purchase_order_number_submit_button')
			self.wait_until_visible('purchase_order_view_title')
	
			# Here he sees a section of the purchase order information: supplier, supplier ref, order number
			self.assertIn('supplier: Stark Industries', self.browser.page_source)
			self.assertIn('supplier ref: 1', self.browser.page_source)
			self.assertIn('Purchase Order No: '+str(4000+today_1_order_no), self.browser.page_source)
	
			# He also sees a table with a row containing: description, fullname, delivery_location, price, status, order_date, delivery_date, quantity and job for each item
			item_row = self.browser.find_element_by_id(f'PO_item_{today_1_item.pk}')
			self.assertIn(f'{today_1_item.description}', item_row.get_attribute("innerHTML"))
			self.assertIn(f'{today_1_item.fullname}', item_row.get_attribute("innerHTML"))
			self.assertIn(f'{today_1_item.delivery_location}', item_row.get_attribute("innerHTML"))
			self.assertIn(f'{today_1_item.quantity}', item_row.get_attribute("innerHTML"))
			self.assertIn(f'{today_1_item.status}', item_row.get_attribute("innerHTML"))
			self.assertIn(f'{today_1_item.order_date}', item_row.get_attribute("innerHTML"))
			self.assertIn(f'{today_1_item.delivery_date}', item_row.get_attribute("innerHTML"))
			self.assertIn(f'{today_1_item.quantity}', item_row.get_attribute("innerHTML"))
			self.assertIn(f'{today_1_item.job.address}', item_row.get_attribute("innerHTML"))
	
			# Marek navigates to the en-route panel of the job and sees all three items in the en-route panel
			self.browser.get(self.live_server_url+reverse('job', kwargs={'job_id':'200ParkAvenue'}))
			self.wait_until_visible('notes_panel')
			self.click('en_route_panel_toggle')
			self.wait_until_visible('en_route_panel')
			# Marek clicks on 'today fname 2'
			self.click(f'po_link_item_{today_2_item.pk}')
	
			# Marek finds he is redirected to the purchase order view of 'today 2' and (as above) all correct information is present
			self.wait_until_visible('purchase_order_view_title')
			self.assertIn('supplier: Stark Industries', self.browser.page_source)
			self.assertIn('supplier ref: 2', self.browser.page_source)
			self.assertIn('Purchase Order No: '+str(4000+today_2_order_no), self.browser.page_source)
	
			item_row = self.browser.find_element_by_id(f'PO_item_{today_2_item.pk}')
			self.assertIn(f'{today_2_item.description}', item_row.get_attribute("innerHTML"))
			self.assertIn(f'{today_2_item.fullname}', item_row.get_attribute("innerHTML"))
			self.assertIn(f'{today_2_item.delivery_location}', item_row.get_attribute("innerHTML"))
			self.assertIn(f'{today_2_item.quantity}', item_row.get_attribute("innerHTML"))
			self.assertIn(f'{today_2_item.status}', item_row.get_attribute("innerHTML"))
			self.assertIn(f'{today_2_item.order_date}', item_row.get_attribute("innerHTML"))
			self.assertIn(f'{today_2_item.delivery_date}', item_row.get_attribute("innerHTML"))
			self.assertIn(f'{today_2_item.quantity}', item_row.get_attribute("innerHTML"))
			self.assertIn(f'{today_2_item.job.address}', item_row.get_attribute("innerHTML"))
	
			# Marek navigates back to the job view and marks 'today 3' as 'on site'
			self.browser.get(self.live_server_url+reverse('job', kwargs={'job_id':'200ParkAvenue'}))
			self.wait_until_visible('notes_panel')
			self.click('en_route_panel_toggle')
			self.wait_until_visible('en_route_panel')
			self.click(base_element=f'en_route_item_{today_3_item.pk}', element='delivered_button')
	
			# Marek clicks the item name in the on-site panel of a job and it redirects to its purchase order view
			self.wait_until_visible('notes_panel')
			self.click('on_site_panel_toggle')
			self.wait_until_visible('on_site_panel')
	
			self.click(f'po_link_item_{today_3_item.pk}')
	
			# Marek finds he is redirected to the purchase order view of 'today 3' and (as above) all correct information is present
			self.wait_until_visible('purchase_order_view_title')
			self.assertIn('supplier: Stark Industries', self.browser.page_source)
			self.assertIn('supplier ref: 3', self.browser.page_source)
			self.assertIn('Purchase Order No: '+str(4000+today_3_order_no), self.browser.page_source)

			today_3_item = Items.objects.filter(description='today 3').first()

			item_row = self.browser.find_element_by_id(f'PO_item_{today_3_item.pk}')
			self.assertIn(f'{today_3_item.description}', item_row.get_attribute("innerHTML"))
			self.assertIn(f'{today_3_item.fullname}', item_row.get_attribute("innerHTML"))
			self.assertIn(f'{today_3_item.delivery_location}', item_row.get_attribute("innerHTML"))
			self.assertIn(f'{today_3_item.quantity}', item_row.get_attribute("innerHTML"))
			self.assertIn(f'{today_3_item.status}', item_row.get_attribute("innerHTML"))
			self.assertIn(f'{today_3_item.order_date}', item_row.get_attribute("innerHTML"))
			self.assertIn(f'{today_3_item.delivery_date}', item_row.get_attribute("innerHTML"))
			self.assertIn(f'{today_3_item.quantity}', item_row.get_attribute("innerHTML"))
			self.assertIn(f'{today_3_item.job.address}', item_row.get_attribute("innerHTML"))
	
			# Marek clicks the item link in the 'today deliveries' panel of the home page and finds he is redirected to the correct po view
			self.browser.get(self.live_server_url+reverse('homepage'))
			self.wait_until_visible('parent_deliveries_panel')
	
			self.click('today_deliveries_panel_toggle')
			self.wait_until_visible('today_deliveries_panel')
	
			self.click(f'po_link_item_{today_1_item.pk}')
	
			self.wait_for(lambda: self.assertEqual(self.live_server_url+reverse('purchase_orders', kwargs={'order_no':today_1_item.PO.id}), self.browser.current_url))
	
			# Marek goes back to the home page and clicks an item in the 'this week' panel
			self.browser.get(self.live_server_url+reverse('homepage'))
			self.wait_until_visible('parent_deliveries_panel')
	
			self.click('this_week_deliveries_panel_toggle')
			self.wait_until_visible('this_week_deliveries_panel')
	
			self.click(f'po_link_item_{today_2_item.pk}')
	
			self.wait_for(lambda: self.assertEqual(self.live_server_url+reverse('purchase_orders', kwargs={'order_no':today_2_item.PO.id}), self.browser.current_url))

			# Marek goes back to the home page and clicks an item on the 'all deliveries' panel
			self.browser.get(self.live_server_url+reverse('homepage'))
			self.wait_until_visible('parent_deliveries_panel')
	
			self.click('all_deliveries_panel_toggle')
			self.wait_until_visible('all_deliveries_panel')
	
			self.click(f'po_link_item_{today_4_item.pk}')
	
			self.wait_for(lambda: self.assertEqual(self.live_server_url+reverse('purchase_orders', kwargs={'order_no':today_4_item.PO.id}), self.browser.current_url))			


