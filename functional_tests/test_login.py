from .base import FunctionalTest
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from sensitive import test_data
from django.test import tag
from django.urls import reverse
from home.models import Site_info


class LoginTest(FunctionalTest):

	#-- HELPER METHODS --#

	def correct_login(self): 
		# to be used on the login screen
		self.wait_for(lambda: self.browser.find_element_by_id('passwordbox'))
		self.browser.find_element_by_id('passwordbox').send_keys(test_data['super'])
		self.browser.find_element_by_id('passwordbox').send_keys(Keys.ENTER)	

	def incorrect_login(self):
		# to be used on the login screen
		self.wait_for(lambda: self.browser.find_element_by_id('passwordbox'))
		self.browser.find_element_by_id('passwordbox').send_keys('incorrect password')
		self.browser.find_element_by_id('passwordbox').send_keys(Keys.ENTER)

	def trigger_lockdown(self):
		# to be used on the login screen
		a = 6
		while a > 0:
			self.incorrect_login()
			a -= 1


	#-- TESTS --#

	def test_logged_out_redirects_to_login_page(self):
		# Yousif navigates to the home page in his browser
		self.browser.get(self.live_server_url)
		
		# Yousif finds he is redirected to the login page as he is not logged in
		self.wait_for(lambda: self.browser.find_element_by_id('passwordbox'))


	@tag('correct_password')
	def test_successfull_login_redirects_to_home_page(self):
		# Yousif navigates to the home page in his browser and is redirected to the loginpage
		self.browser.get(self.live_server_url)
		self.wait_for(lambda: self.browser.find_element_by_id('passwordbox')) # REFRACT - assert the url not html, this line repeats in the login method
		self.browser.refresh()

		self.correct_login()

		self.wait_for(lambda: self.assertEquals(self.browser.title, 'TopMarks - Home'))
		self.browser.refresh()

	@tag('incorrect_password_counter')
	def test_incorrect_password_gives_correct_error(self):
		self.tearDown()
		self.setUp()
		# Yousif navigates to the home page and inputs the incorrect password
		self.browser.get(self.live_server_url)
		self.incorrect_login()

		# The page re-renders and Yousif finds an alert saying 'Incorrect password, 5 attempts remaining'	
		self.wait_for(lambda: self.assertIn('Incorrect password, 5 attempts remaining', self.browser.page_source))
		# Yousif puts the incorrect password again 4 more times and each time finds the error message incrementally reducing his remaining attempts by 1 each time until it says 1 attempts remaining
		a = 4
		while a >= 1:
			self.incorrect_login()
			self.wait_for(lambda: self.assertIn(f'Incorrect password, {a} attempts remaining', self.browser.page_source))
			a -= 1


	@tag('lockdown')
	def test_fifth_incorrect_password_locks_down_site(self):
		# Yousif navigates to the home page and inputs five incorrect passwords in a row
		self.browser.get(self.live_server_url)
		self.trigger_lockdown()

		# Yousif sees an alert saying 'WEBSITE IS LOCKED' and notices that the passwordbox no longer appears
		self.wait_for(lambda: self.assertIn('WEBSITE IS LOCKED', self.browser.page_source))
		self.wait_for(lambda: self.assertNotIn('passwordbox', self.browser.page_source))

	@tag('lockdown', 'lockdown_unlock')
	def test_unlock_link_unlocks_site(self):
		# Yousif has locked the website by mistake from his browser
		self.browser.get(self.live_server_url)
		self.trigger_lockdown()

		# After checking his email Yousif follows the unlock link to unlock the website
		unlock_link = self.live_server_url + '/unlock/' + Site_info.objects.first().password
		self.browser.get(unlock_link)

		# Perversely, Yousif types the wrong password again, however like normal it says '5 attempts remaining' 
		self.incorrect_login()
		self.wait_for(lambda: self.assertIn('Incorrect password, 5 attempts remaining', self.browser.page_source))

		# Yousif finally types the correct password and gets logged in
		self.correct_login()
		self.wait_for(lambda: self.assertEquals(self.browser.title, 'TopMarks - Home'))
		self.browser.refresh()



# class multiple_browsers_login(LoginTest):




	# NOTE finish designing lockdown and login process before testing with multiple browsers

	# @tag('multiple_browsers')
	# def test_simultaneous_multiple_users_login_integrity(self):
		# yousif_browser = self.browser
		# marek_server_url = 'http://localhost:8000'
		# marek_browser = webdriver.Chrome()
# 
		# # Yousif successfully logs in after being redirected from the home page
		# yousif_browser.get(self.live_server_url)
		# self.correct_login(yousif_browser)
# 
		# self.wait_for(lambda: self.assertEquals(self.browser.title, 'TopMarks - Home')) # REFRACT - should I put this in the login method?
# 
# 		
		# # Marek navigates to the home page in *his* browser
		# marek_browser.get(marek_server_url)
# 
		# # Because Marek isn't logged in yet he finds he is immediately redirected to the login screen
		# self.wait_for(lambda: self.assertEquals(marek_browser.current_url, marek_server_url+reverse('login')))
# 
		# # Marek inputs the incorrect password 5 times and locks down the website
		# self.trigger_lockdown(marek_browser)
		# self.wait_for(lambda: self.assertIn(f'Incorrect password, 1 attempts remaining', marek_browser.page_source))

		# self.fail('integrate lockdown functionality here!')
		# NOTE: Need to RGR the lockdown functionality before completing this test, this is where the 'user story' itself is refracted.


# Marek inputs the incorrect password a 5th time and finds the website is now locked, no password form is visible and it has a message saying 'too many password attempts, an email has been sent to the administartor(s) with a link to unlock TOPAIMS'


# however Yousif is still able to do things as he is already logged in

# coincidentally Yousif decides to close his browser


# when Yousif tries to navigate to the home page he finds he is redirected to the locked password page


# Yousif checks his email and finds that the email has been CCed to Marek, David and Alexander

# Yousif follows the link in his email and finds the password page unlocked


# Marek also finds the password page unlocked

# Both Marek and Yousif enter the correct password and get redirected to the home page


# Yousif is finished with TOPAIMS and closes his browser 