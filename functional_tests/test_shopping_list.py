from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from django.urls import reverse
from home.models import Site_info, Items, Shopping_list_items
from selenium.webdriver.support.ui import Select
import time


class ShoppingListPageTest(FunctionalTest):

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
	#-- SETUP AND TEARDOWN --#

	def setUp(self):
		Site_info.objects.create(locked=False, password='thischangesautomaticallyaftereverylock')
		self.browser = webdriver.Chrome()
		self.login()
		self.create_job()

  #--------------------------------------------------------------#

	def test_shopping_list_page(self):

		# Marek navigates to the shopping list page
		self.browser.get(self.live_server_url + reverse('shopping_list'))
		# Marek sees an empty shopping list with a form on the bottom
		self.wait_for(lambda: self.browser.find_element_by_id('shopping_list_panel'))
		self.wait_for(lambda: self.browser.find_element_by_id('new_shopping_list_item_form'))

		# Marek decides to add a new item to the shopping list

		self.browser.find_element_by_id('new_shopping_list_item_form').find_element_by_id('shopping_list_description_input').send_keys('shopping list item 1')
		self.browser.find_element_by_id('new_shopping_list_item_form').find_element_by_id('shopping_list_quantity_input').send_keys('1')
		shopping_list_job_choice = Select(self.browser.find_element_by_id('new_shopping_list_item_form').find_element_by_id('shopping_list_job_input'))
		shopping_list_job_choice.select_by_value('200 Park Avenue') # may have to change the base elements here to the shopping list panel (not the form)

		self.click(base_element='new_shopping_list_item_form', element='shopping_list_form_submit_button')

		# REFRACT this to find the pk every time for test stability

		# on every shopping list item Marek sees description | quantity | job | acquired
		self.wait_for(lambda: self.browser.find_element_by_id('Shopping_list_items_1')) # id="{ x.model }_{x.pk}"
		self.wait_for(lambda: self.browser.find_element_by_id('Shopping_list_items_1_acquired_button')) # id="{x.model}_{x.pk}_acquired_button"
		new_shopping_list_item = self.browser.find_element_by_id('Shopping_list_items_1')
		self.assertIn('shopping list item 1', new_shopping_list_item.get_attribute("innerHTML"))
		self.assertIn('1', new_shopping_list_item.get_attribute("innerHTML"))
		self.assertIn('200 Park Avenue', new_shopping_list_item.get_attribute("innerHTML"))
		
		# Marek clicks 'acquired' on 'shopping list item 1'
		self.click(base_element='Shopping_list_items_1', element='Shopping_list_items_1_acquired_button')
		# The page reloads and the item is no longer present
		self.wait_for(lambda: self.assertNotIn('id="Shopping_list_items_1"', self.browser.page_source))
		# an alert says 'x acquired'
		self.wait_for(lambda: self.assertIn('shopping list item 1 acquired', self.browser.page_source))

		# AFTER STANDALONE SHOPPING LIST IS WORKING
		# Marek sees 'shopping list item' appear in 'en route' section of job view 200 Park Avenue with status 'acquired'

	def test_shopping_list_synchronisation(self):
		# Marek adds a shopping list item to 200 Park Avenue via the shopping list page
		self.browser.get(self.live_server_url + reverse('shopping_list'))
		self.browser.find_element_by_id('new_shopping_list_item_form').find_element_by_id('shopping_list_description_input').send_keys('shopping list item 2')
		self.browser.find_element_by_id('new_shopping_list_item_form').find_element_by_id('shopping_list_quantity_input').send_keys('1')
		shopping_list_job_choice = Select(self.browser.find_element_by_id('new_shopping_list_item_form').find_element_by_id('shopping_list_job_input'))
		shopping_list_job_choice.select_by_value('200 Park Avenue')
		self.click(base_element='new_shopping_list_item_form', element='shopping_list_form_submit_button')
		time.sleep(1) # REFRACT
		new_shopping_list_model_object = Shopping_list_items.objects.filter(description='shopping list item 2').first()
		SLI_pk = new_shopping_list_model_object.pk # SLI_pk = shopping list item pk

		# Marek then acquires the shopping list item in a shop and clicks 'acquired' in the shopping list view
		self.browser.get(self.live_server_url + reverse('shopping_list'))
		self.click(base_element=f'Shopping_list_items_{SLI_pk}', element=f'Shopping_list_items_{SLI_pk}_acquired_button')
		self.wait_for(lambda: self.assertNotIn('id="Shopping_list_items_1"', self.browser.page_source))

		new_acquired_item_model_object = Items.objects.filter(description='shopping list item 2').first()
		AI_pk = new_acquired_item_model_object.pk # AI_pk = acquired item pk

		# Marek sees 'shopping list item 2' and the quantity in the 'en-route' section of the job view for 200 Park Avenue with status 'ACQUIRED'
		self.browser.get(self.live_server_url + reverse('job', kwargs={'job_id':'200ParkAvenue'}))
		self.wait_for(lambda: self.browser.find_element_by_id('en_route_panel_toggle'))
		self.click('en_route_panel_toggle')
		en_route_acquired_item = self.browser.find_element_by_id('en_route_panel').find_element_by_id(f'en_route_item_{AI_pk}') # x = Item.pk (remember, acuiring deletes the shopping list item and creates a new Items item)
		self.assertIn('shopping list item 2', en_route_acquired_item.get_attribute("innerHTML"))
		self.assertIn('ACQUIRED', en_route_acquired_item.get_attribute("innerHTML"))
		self.browser.refresh()