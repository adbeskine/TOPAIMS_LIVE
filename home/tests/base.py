from django.test import TestCase
from sensitive import user_passwords, test_data
from django.urls import reverse
from home.models import Site_info

class Test(TestCase):

	#-- HELPER METHODS --#

	def login(self):
		self.client.post('/login/', {'password':test_data['super']}, follow=True) # <- for backwards compatability with older tests

	def loginSuper(self):
		self.client.post('/login/', {'password':test_data['super']}, follow=True)

	def loginManager(self):
		self.client.post('/login/', {'password':test_data['manager']}, follow=True)

	def loginStaff(self):
		self.client.post('/login/', {'password':test_data['staff']}, follow=True)


	def logout(self):
		self.client.session['logged_in'] = False
		self.client.session.save()

	#-- SETUP AND TEARDOWN --#

	def setUp(self):
		Site_info.objects.create(locked=False, password='thischangesautomaticallyaftereverylock')


