from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from home.models import Site_info, Items, Jobs
from django.urls import reverse
from selenium.webdriver.support.ui import Select


class JobsViewTest(FunctionalTest):

	#-- HELPER METHODS --#
	def create_custom_job(self, name, email, phone, address, note, status): # REFRACT make this actually create db objects instead of manually typing everything
		self.browser.get(self.live_server_url + reverse('new_job_form'))
		self.browser.find_element_by_id('Name').send_keys(name)
		self.browser.find_element_by_id('Email').send_keys(email)
		self.browser.find_element_by_id('Phone').send_keys(phone)
		self.browser.find_element_by_id('Address').send_keys(address)
		self.browser.find_element_by_id('Note').send_keys(note)
		ActionChains(self.browser).click(self.browser.find_element_by_id('create')).perform()
		self.wait_for(lambda: self.assertEqual(self.browser.title, f'TopMarks - {address}'))

		new_job = Jobs.objects.filter(address=address).first()
		new_job.status=status
		new_job.save()

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

	def wait_until_visible(self, element, base_element=None):
		if base_element:
			return self.wait_for(lambda: self.assertTrue(self.browser.find_element_by_id(base_element).find_element_by_id(element).is_displayed()))
		else:
			return self.wait_for(lambda: self.assertTrue(self.browser.find_element_by_id(element).is_displayed()))


	#-- SETUP AND TEARDOWN --#

	def setUp(self):
			Site_info.objects.create(locked=False, password='thischangesautomaticallyaftereverylock')
			self.browser = webdriver.Chrome()
			self.login(self.browser)

	#---------------------------------------------------------------------------------#

	def test_adding_new_job(self):

		# Marek navigates to the job view, opens the quotes section and clicks the plus button
		self.browser.get(self.live_server_url + reverse('jobs'))
		self.click(base_element='all_jobs_panel', element='quote_jobs_panel_toggle')
		self.wait_until_visible('create_job_button')
		self.click('create_job_button')
	
		# marek finds he is redirected to the new job form
		self.wait_for(lambda: self.assertEqual(self.browser.current_url, self.live_server_url + reverse('new_job_form')))
		self.wait_for(lambda: self.assertEqual(self.browser.title, 'TopMarks - New Job Form'))
	
		# Marek fills the form with the client's name, contact details and a few notes and clicks 'CREATE'
		self.browser.find_element_by_id('Name').send_keys('Tony Stark')
		self.browser.find_element_by_id('Email').send_keys('Tony@StarkIndustries.net')
		self.browser.find_element_by_id('Phone').send_keys('01234567899')
		self.browser.find_element_by_id('Address').send_keys('200 Park Avenue') #MVP for multiple jobs at different times just add a quick bullet note in the adress
		self.browser.find_element_by_id('Note').send_keys("don't ignore JARVIS, he's temperemental and finds it rude")
		ActionChains(self.browser).click(self.browser.find_element_by_id('create')).perform()
	
		# Marek finds he is redirected to the job view of the newly created job
		self.wait_for(lambda: self.assertEqual(self.browser.title, 'TopMarks - 200 Park Avenue'))

	
	def test_jobs_view_job_presentation(self):

		# Marek has been using the software for a long time now and quite a lot of data has aggregated, with the software he has completed 2 jobs,
		# 4 jobs are ongoing and he has put out 1 quote || REFRACT: use real examples, schedule of items etc, full fledged details, notes, everything, this state can also be used for demonstrations
		self.create_custom_job(name='Tony Stark', email='Tony@StarkIndustries.net', phone='01234567898', address='200 Park Avenue', status='completed', note=
			'job completed')
		self.create_custom_job(name='Nick Fury', email='NF@SHIELD.com', phone='01234567898', address='59th Madison Avenue', status='completed', note='job completed')
	
		self.create_custom_job(name='Peter Parker', email='pparker@dailybugle.com', phone='01234567898', address='175 Fifth Avenue', status='ongoing', note='job ongoing')
		self.create_custom_job(name='Stephen Strange', email='strange@NYPH.org', phone='012346567898', address='177A Bleecker Street', status='ongoing', note='job ongoing')
		self.create_custom_job(name='Matt Murdock', email='mmurdoch@NelsonandMurdock.org', phone='01234567898', address='Hells Kitchen', status='ongoing', note='job ongoing')
		self.create_custom_job(name='Luke Cage', email='luke__cage@hotmail.com', phone='01234567898', address='Gem Theater 42nd Street', status='ongoing', note='job ongloing')
	
		self.create_custom_job(name='Jessica Jones', email='JJ@aliasinvestigations.com', phone='01234567898', address='Alias Investigations Office', status='quote', note='job quote')
	
		
		# When the page loads Marek sees all the ongoing jobs as default in the ongoing jobs panel
		self.browser.get(self.live_server_url+reverse('jobs'))
		self.wait_until_visible(base_element='all_jobs_panel', element='ongoing_jobs_panel')
		ongoing_jobs_panel = self.browser.find_element_by_id('all_jobs_panel').find_element_by_id('ongoing_jobs_panel')
		
		self.assertIn('175 Fifth Avenue', ongoing_jobs_panel.get_attribute("innerHTML"))
		self.assertIn('177A Bleecker Street', ongoing_jobs_panel.get_attribute("innerHTML"))
		self.assertIn('Hells Kitchen', ongoing_jobs_panel.get_attribute("innerHTML"))
		self.assertIn('Gem Theater 42nd Street', ongoing_jobs_panel.get_attribute("innerHTML"))

		# Marek sees there are three tabs to choose from 'ongoing', 'completed', 'jobs'.
		self.wait_until_visible(base_element='all_jobs_panel', element='ongoing_jobs_panel_toggle')
		self.wait_until_visible(base_element='all_jobs_panel', element='completed_jobs_panel_toggle')
		self.wait_until_visible(base_element='all_jobs_panel', element='quote_jobs_panel_toggle')

		# Marek sees that all the completed jobs are present in the completed jobs panel
		self.click(base_element='all_jobs_panel', element='completed_jobs_panel_toggle')
		self.wait_until_visible(base_element='all_jobs_panel', element='completed_jobs_panel')
		completed_jobs_panel = self.browser.find_element_by_id('all_jobs_panel').find_element_by_id('completed_jobs_panel')

		self.assertIn('200 Park Avenue', completed_jobs_panel.get_attribute("innerHTML"))
		self.assertIn('59th Madison Avenue', completed_jobs_panel.get_attribute("innerHTML"))

		# Marek sees that all the quotes are present in the quote jobs panel
		self.click(base_element='all_jobs_panel', element='quote_jobs_panel_toggle')
		self.wait_until_visible(base_element='all_jobs_panel', element='quote_jobs_panel')
		quote_jobs_panel = self.browser.find_element_by_id('all_jobs_panel').find_element_by_id('quote_jobs_panel')

		self.assertIn('Alias Investigations Office', quote_jobs_panel.get_attribute("innerHTML"))


	def test_job_card_goes_to_correct_job_profile(self):
		#when marek clicks on one of the displayed jobs in the jobs view it redirects to the correct job
		self.create_job()
		job = Jobs.objects.filter(address='200 Park Avenue').first()
		self.browser.get(self.live_server_url+reverse('jobs'))
		self.wait_until_visible('all_jobs_panel')
		self.click(base_element='all_jobs_panel', element='quote_jobs_panel_toggle')

		self.click(base_element='quote_jobs_panel', element=f'job_link_{job.pk}')

		self.wait_for(lambda: self.assertEqual(self.browser.title, 'TopMarks - 200 Park Avenue'))










# Marek sees that all the jobs are listed in reverse chronological order in their respective tab/section || POST MVP

# Marek finds that the colour of the ongoing jobs are a deep blue || POST MVP

# Marek sees that the colour of the completed jobs are red || POST MVP

# Marek sees that the colour of the quotes are clear/white || POST MVP

# Marek finds that when he hovers his mouse over a job profile the client's contact details appear || (disable this in client view?) || POST MVP
