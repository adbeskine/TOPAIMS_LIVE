from selenium import webdriver
from sensitive import test_data
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.common.exceptions import WebDriverException
import time
from home.models import Site_info
from django.urls import reverse
from selenium.webdriver.common.keys import Keys
import time


########################
#   FUNCTIONAL TESTS   #
########################

class FunctionalTest(StaticLiveServerTestCase):


	def setUp(self):
		Site_info.objects.create(locked=False, password='thischangesautomaticallyaftereverylock')
		self.browser = webdriver.Chrome()

	def tearDown(self):
		self.browser.refresh()
		self.browser.quit()

	#----- HELPER METHODS -----#

	def wait_for(self, func):
		MAX_WAIT = 10
		start_time = time.time()
		while True:
			try:
				return func()
			except(AssertionError, WebDriverException) as e:
				if time.time() - start_time > MAX_WAIT:
					self.browser.refresh()
					raise e
				time.sleep(0.5)

	def login(self): # <- keep for backwards compatability with older tests
		self.browser.get(self.live_server_url + reverse('login'))
		self.wait_for(lambda: self.browser.find_element_by_id('passwordbox'))
		self.browser.find_element_by_id('passwordbox').send_keys(test_data['super'])
		self.browser.find_element_by_id('passwordbox').send_keys(Keys.ENTER)
		self.browser.refresh() # teardown issue when running on localhost, need to refresh before browser quits every time

	def loginSuper(self):
		self.browser.get(self.live_server_url + reverse('login'))
		self.wait_for(lambda: self.browser.find_element_by_id('passwordbox'))
		self.browser.find_element_by_id('passwordbox').send_keys(test_data['super'])
		self.browser.find_element_by_id('passwordbox').send_keys(Keys.ENTER)
		self.browser.refresh()

	def loginManager(self):
		self.browser.get(self.live_server_url + reverse('login'))
		self.wait_for(lambda: self.browser.find_element_by_id('passwordbox'))
		self.browser.find_element_by_id('passwordbox').send_keys(test_data['manager'])
		self.browser.find_element_by_id('passwordbox').send_keys(Keys.ENTER)
		self.browser.refresh()

	def loginStaff(self):
		self.browser.get(self.live_server_url + reverse('login'))
		self.wait_for(lambda: self.browser.find_element_by_id('passwordbox'))
		self.browser.find_element_by_id('passwordbox').send_keys(test_data['staff'])
		self.browser.find_element_by_id('passwordbox').send_keys(Keys.ENTER)
		self.browser.refresh()
