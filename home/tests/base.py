from django.test import TestCase
from sensitive import WEBSITE_PASSWORD as password
from django.urls import reverse
from home.models import Site_info

class Test(TestCase):

	#-- HELPER METHODS --#

	def login(self):
		self.client.post('/login/', {'password': password}, follow=True)


	def logout(self):
		self.client.session['logged_in'] = False
		self.client.session.save()

	#-- SETUP AND TEARDOWN --#

	def setUp(self):
		Site_info.objects.create(locked=False, password='thischangesautomaticallyaftereverylock')


