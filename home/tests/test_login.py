from .base import Test
from django.test import TestCase
from sensitive import WEBSITE_PASSWORD as password
from django.urls import reverse
from home.models import Site_info

class LoginPageTest(Test):

	#-- HELPER METHODS --#

	def post_correct_password(self):
		self.loginSuper()

	def post_incorrect_password(self):
		self.client.post('/login/', {'password': 'incorrect password'}, follow=True)

	#-- TESTS --#

	def test_homepage_redirects_logged_out_user(self):
		
		response=self.client.get('/', follow=True)

		self.assertRedirects(response, reverse('login'))
		self.assertTemplateUsed(response, 'home/login.html')

	def test_logged_out_user_can_log_in(self):
		response=self.client.get('/', follow=True)
		self.assertRedirects(response, reverse('login'))
		
		self.post_correct_password()

		self.assertEquals(self.client.session['logged_in'], True)

	def test_user_redirected_to_home_page_after_login(self):
		self.client.get('/', follow=True)
		
		response = self.post_correct_password()

		self.assertTemplateNotUsed(response, 'home/login.html')
		self.assertTemplateUsed(response, 'home/home.html')


	def test_incorrect_password_attempts_are_logged_correctly(self):
		self.client.get('/', follow=True)

		response = self.post_incorrect_password()
		self.assertEquals(self.client.session['incorrect_password_attempts'], 0)

		response = self.post_incorrect_password()
		self.assertEquals(self.client.session['incorrect_password_attempts'], 1)


class LockdownTest(LoginPageTest):

	#-- HELPER METHODS --#
	def lock_site(self):
		for i in range(0, 6):
			self.post_incorrect_password()

	#-- TESTS --#

	def test_5_incorrect_password_changes_site_status_to_locked(self):
		self.lock_site()

		site = Site_info.objects.first()
		self.assertEquals(site.locked, True)


	def test_locked_site_will_not_load_for_logged_out_users(self):
		self.lock_site()

		response = self.client.get(reverse('homepage'), follow=True)

		self.assertContains(response, 'WEBSITE IS LOCKED', status_code=200)


	def test_password_link_unlocks_site(self):
		self.lock_site()
		unlock_password = Site_info.objects.first().password

		self.client.post(reverse('unlock', kwargs={'unlock_password':unlock_password}))

		site = Site_info.objects.first()
		self.assertEquals(site.locked, False)
		self.assertNotEquals(site.password, unlock_password)

	def test_incorrect_password_attempts_reset_after_unlock(self):
		self.lock_site()

		unlock_password = Site_info.objects.first().password
		self.client.post(reverse('unlock', kwargs={'unlock_password':unlock_password}))

		self.assertRaises(KeyError, lambda: self.client.session['incorrect_password_attempts'])





