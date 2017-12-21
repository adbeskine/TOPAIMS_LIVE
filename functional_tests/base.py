from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.common.exceptions import WebDriverException
import time
from django.urls import reverse
from selenium.webdriver.common.keys import Keys
import time

from _Auth.models import Site_info, Pass

staff_password = Pass.objects.filter(user='staff').first().password
manager_password = Pass.objects.filter(user='manager').first().password
super_password = Pass.objects.filter(user='super').first().password


########################
#   FUNCTIONAL TESTS   #
########################

class FunctionalTest(StaticLiveServerTestCase):

	#----- HELPER METHODS -----#
	def setup_site_info(self):
		Site_info.objects.create(locked=False, password='thischangesautomaticallyaftereverylock')

	def setup_users(self):
		Pass.objects.create(password='staffPassword', user='staff')
		Pass.objects.create(password='managerPassword', user='manager')
		Pass.objects.create(password='superPassword', user='super')

	def setup_system(self):
		self.setup_site_info()
		self.setup_users()
		self.browser = webdriver.Chrome()

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

	def login(self): # <- keep for backwards compatability with older tests, make sure this is super user
		self.browser.get(self.live_server_url + reverse('login'))
		self.wait_for(lambda: self.browser.find_element_by_id('passwordbox'))
		self.browser.find_element_by_id('passwordbox').send_keys(Pass.objects.filter(user='super').first().password)
		self.browser.find_element_by_id('passwordbox').send_keys(Keys.ENTER)
		self.browser.refresh() # teardown issue when running on localhost, need to refresh before browser quits every time

	def loginSuper(self):
		self.browser.get(self.live_server_url + reverse('login'))
		self.wait_for(lambda: self.browser.find_element_by_id('passwordbox'))
		self.browser.find_element_by_id('passwordbox').send_keys(Pass.objects.filter(user='super').first().password)
		self.browser.find_element_by_id('passwordbox').send_keys(Keys.ENTER)
		self.browser.refresh()

	def loginManager(self):
		self.browser.get(self.live_server_url + reverse('login'))
		self.wait_for(lambda: self.browser.find_element_by_id('passwordbox'))
		self.browser.find_element_by_id('passwordbox').send_keys(Pass.objects.filter(user='manager').first().password)
		self.browser.find_element_by_id('passwordbox').send_keys(Keys.ENTER)
		self.browser.refresh()

	def loginStaff(self):
		self.browser.get(self.live_server_url + reverse('login'))
		self.wait_for(lambda: self.browser.find_element_by_id('passwordbox'))
		self.browser.find_element_by_id('passwordbox').send_keys(Pass.objects.filter(user='staff').first().password)
		self.browser.find_element_by_id('passwordbox').send_keys(Keys.ENTER)
		self.browser.refresh()

	#-- SETUP AND TEARDOWN --#

	def setUp(self):
		self.setup_system()

	def tearDown(self):
		self.browser.refresh()
		self.browser.quit()

