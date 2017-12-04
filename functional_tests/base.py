from selenium import webdriver
from sensitive import WEBSITE_PASSWORD as password
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.common.exceptions import WebDriverException
import time
from home.models import Site_info
from django.urls import reverse
from selenium.webdriver.common.keys import Keys


########################
#   FUNCTIONAL TESTS   #
########################

class FunctionalTest(StaticLiveServerTestCase):


	def setUp(self):
		Site_info.objects.create(locked=False, password='thischangesautomaticallyaftereverylock')
		self.browser = webdriver.Chrome()

	def tearDown(self):
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
					raise e
				time.sleep(0.5)

	def login(self, browser):
		browser.get(self.live_server_url + reverse('login'))
		self.wait_for(lambda: browser.find_element_by_id('passwordbox'))
		browser.find_element_by_id('passwordbox').send_keys(password)
		browser.find_element_by_id('passwordbox').send_keys(Keys.ENTER)
