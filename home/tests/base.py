from django.test import TestCase
from django.urls import reverse
from _Auth.models import Site_info, Pass

class Test(TestCase):

	#-- HELPER METHODS --#

	def login(self):
		self.client.post('/login/', {'password':Pass.objects.filter(user='super').first().password}, follow=True) # <- for backwards compatability with older tests

	def loginSuper(self):
		self.client.post('/login/', {'password':Pass.objects.filter(user='super').first().password}, follow=True)

	def loginManager(self):
		self.client.post('/login/', {'password':Pass.objects.filter(user='manager').first().password}, follow=True)

	def loginStaff(self):
		self.client.post('/login/', {'password':Pass.objects.filter(user='staff').first().password}, follow=True)


	def logout(self):
		self.client.session['logged_in'] = False
		self.client.session.save()

	def setup_site_info(self):
		Site_info.objects.create(locked=False, password='thischangesautomaticallyaftereverylock')

	def setup_users(self):
		Pass.objects.create(password='staffPassword', user='staff')
		Pass.objects.create(password='managerPassword', user='manager')
		Pass.objects.create(password='superPassword', user='super')

	def setup_system(self):
		self.setup_site_info()
		self.setup_users()

	#-- SETUP AND TEARDOWN --#

	def setUp(self):
		self.setup_system()

