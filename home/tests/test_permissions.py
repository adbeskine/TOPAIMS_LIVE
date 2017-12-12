from .base import Test
from django.urls import reverse
from django.conf import settings
from home.models import Site_info, Jobs, Notes, Scheduled_items, Purchase_orders, Items, Shopping_list_items


class PermissionsTest(Test):

	# this tests goes through every single backend CRUD function, as every type of user and tests the permissons enforcement accordingly
	# REFRACT - currently due to time constraints this will only enforce on the back end the delete permissions, the CRU permissions are enforced on the front end as users with lower permissions physically don't see the buttons needed to do things. When have time DO add here for integrity's sake
	# further from above, looking at the permissions table, the only update function that needs to really be enforced here is the updating of notes - which hasn't been developed yet.

	#-- HELPER METHODS --#
	
	def create_custom_job(self, name, email, phone, address, note):
		form_data = {
		'Name':name,
		'Email':email,
		'Phone':phone,
		'Address':address,
		'Note':note,
		}

		response = self.client.post(reverse('new_job_form'), form_data, follow=True)
	
	def create_shopping_list_item(self, description, quantity, job):

  		new_shopping_list_item_data = {
  			'description':description,
  			'job':job.address,
  			'quantity':1
  		}
  		self.client.post(reverse('shopping_list_create', kwargs={'function':'create'}), data=new_shopping_list_item_data, follow=True)
	
	def create_acquired_shopping_list_item(self, description, quantity, job):

		self.create_shopping_list_item(description, quantity, job)
		shopping_list_item = Shopping_list_items.objects.filter(description=description).first()
		self.client.get(reverse('acquired', kwargs={'pk':shopping_list_item.pk}), follow=True)
	
	def create_schedule_item(self, description, date_1, quantity, job, date_2=None):
		
		if date_2:	
			schedule_item_form_data = {
				'description':description,
				'date_1':date_1,
				'date_2':date_2,
				'quantity':quantity
				}

			return self.client.post(reverse('new_schedule_item', kwargs={'job_id':job.job_id}), data=schedule_item_form_data, follow=True)

		else:
			schedule_item_form_data = {
				'description':description,
				'date_1':date_1,
				'quantity':quantity
				}

			return self.client.post(reverse('new_schedule_item', kwargs={'job_id':job.job_id}), data=schedule_item_form_data, follow=True)

	def create_job_note(self, title, text, job):
		note_form_data = {
			'Title':title,
			'Text':text
		}
		self.client.post(reverse('new_note', kwargs={'job_id':job.job_id}), data=note_form_data, follow=True)
	
	def create_admin_note(self, title, text):
		note_form_data = {
			'Title':title,
			'Text':text
		}
		self.client.post(reverse('new_note', kwargs={'job_id':'admin'}), data=note_form_data, follow=True)

	def create_purchase_order(
		self, Supplier='Strark Industries', Supplier_ref='123',
		description1=None, fullname1=None, delivery_date1=None, quantity1=None, price1=None, job1=None, delivery_location1=None,
		description2=None, fullname2=None, delivery_date2=None, quantity2=None, price2=None, job2=None, delivery_location2=None,
		description3=None, fullname3=None, delivery_date3=None, quantity3=None, price3=None, job3=None, delivery_location3=None,
		description4=None, fullname4=None, delivery_date4=None, quantity4=None, price4=None, job4=None, delivery_location4=None,
		description5=None, fullname5=None, delivery_date5=None, quantity5=None, price5=None, job5=None, delivery_location5=None,
		description6=None, fullname6=None, delivery_date6=None, quantity6=None, price6=None, job6=None, delivery_location6=None,
		description7=None, fullname7=None, delivery_date7=None, quantity7=None, price7=None, job7=None, delivery_location7=None,
		description8=None, fullname8=None, delivery_date8=None, quantity8=None, price8=None, job8=None, delivery_location8=None,
		description9=None, fullname9=None, delivery_date9=None, quantity9=None, price9=None, job9=None, delivery_location9=None,
		description10=None, fullname10=None, delivery_date10=None, quantity10=None, price10=None, job10=None, delivery_location10=None,
		):
		
		PO_data = {
		'Supplier':Supplier,
		'Supplier_ref':Supplier_ref,
		'item_1_description':description1,
		'item_1_fullname':fullname1,
		'item_1_delivery_location':(delivery_location1,),
		'item_1_job':job1.address,
		'item_1_delivery_date':delivery_date1, #must be date object.
		'item_1_quantity':quantity1,
		'item_1_price':price1,
		}

		if description2:
			PO_data.update({
				'item_2_description':description2,
				'item_2_fullname':fullname2,
				'item_2_delivery_location':(delivery_location2,),
				'item_2_job':job2.address,
				'item_2_delivery_date':delivery_date2, #must be date object.
				'item_2_quantity':quantity2,
				'item_2_price':price2,
					})

		if description3:
			PO_data.update({
				'item_3_description':description3,
				'item_3_fullname':fullname3,
				'item_3_delivery_location':(delivery_location3,),
				'item_3_job':job3.address,
				'item_3_delivery_date':delivery_date3, #must be date object.
				'item_3_quantity':quantity3,
				'item_3_price':price3,
					})

		if description4:
			PO_data.update({
				'item_4_description':description4,
				'item_4_fullname':fullname4,
				'item_4_delivery_location':(delivery_location4,),
				'item_4_job':job4.address,
				'item_4_delivery_date':delivery_date4, #must be date object.
				'item_4_quantity':quantity4,
				'item_4_price':price4,
					})

		if description5:
			PO_data.update({
				'item_5_description':description5,
				'item_5_fullname':fullname5,
				'item_5_delivery_location':(delivery_location5,),
				'item_5_job':job5.address,
				'item_5_delivery_date':delivery_date5, #must be date object.
				'item_5_quantity':quantity5,
				'item_5_price':price5,
					})

		if description6:
			PO_data.update({
				'item_6_description':description6,
				'item_6_fullname':fullname6,
				'item_6_delivery_location':(delivery_location6,),
				'item_6_job':job6.address,
				'item_6_delivery_date':delivery_date6, #must be date object.
				'item_6_quantity':quantity6,
				'item_6_price':price6,
					})

		if description7:
			PO_data.update({
				'item_7_description':description7,
				'item_7_fullname':fullname7,
				'item_7_delivery_location':(delivery_location7,),
				'item_7_job':job7.address,
				'item_7_delivery_date':delivery_date7, #must be date object.
				'item_7_quantity':quantity7,
				'item_7_price':price7,
					})

		if description8:
			PO_data.update({
				'item_8_description':description8,
				'item_8_fullname':fullname8,
				'item_8_delivery_location':(delivery_location8,),
				'item_8_job':job8.address,
				'item_8_delivery_date':delivery_date8, #must be date object.
				'item_8_quantity':quantity8,
				'item_8_price':price8,
					})

		if description9:
			PO_data.update({
				'item_9_description':description9,
				'item_9_fullname':fullname9,
				'item_9_delivery_location':(delivery_location9,),
				'item_9_job':job9.address,
				'item_9_delivery_date':delivery_date9, #must be date object.
				'item_9_quantity':quantity9,
				'item_9_price':price9,
					})

		if description10:
			PO_data.update({
				'item_10_description':description10,
				'item_10_fullname':fullname10,
				'item_10_delivery_location':(delivery_location10,),
				'item_10_job':job10.address,
				'item_10_delivery_date':delivery_date10, #must be date object.
				'item_10_quantity':quantity10,
				'item_10_price':price10,
					})

		self.client.post(reverse('purchase_order_homepage'), data=PO_data, follow=True)

	def check_get_redirects(self, urlname):
		self.client.get(reverse('homepage'))
		response = self.client.get(urlname)
		self.assertRedirects(response, reverse('homepage'))


	def setUp(self):
		now = settings.NOW
		Site_info.objects.create(locked=False, password='thischangesautomaticallyaftereverylock')
		self.loginSuper()

		# Job 1
		self.create_custom_job(name='Tony Stark', email='Tony@StarkIndustries.net', phone='01234567898', address='200 Park Avenue', note='this is job 1')
		job1 = Jobs.objects.filter(address='200 Park Avenue').first()

		# shopping list items 1
		self.create_shopping_list_item('job 1 shopping list item 1', 1, job1)

		# acquired shopping list items 1
		self.create_acquired_shopping_list_item('job 1 acquired shopping list item 1', 1, job1)

		# purchase order with 1 item
		self.create_purchase_order(
			description1='job 1 purchase order 1 item 1 description',
			fullname1='job 1 purchase order 1 item 1 fullname',
			delivery_date1=now,
			quantity1=1,
			price1=100,
			job1=job1,
			delivery_location1='shop',
			)

		# Job note 1
		self.create_job_note('job 1 note 1 title', 'job 1 note 1 text', job1)

		# admin note 1
		self.create_admin_note('admin note 1 title', 'admin note 1 text')

	def test_visibility_permissions_staff(self):
		PO_item = Items.objects.filter(description='job 1 purchase order 1 item 1 description').first()
		self.loginStaff()

		
		self.check_get_redirects(urlname=reverse('new_job_form'))

		self.check_get_redirects(urlname=reverse('purchase_orders', kwargs={'order_no':PO_item.PO.order_no}))

		self.check_get_redirects(urlname=reverse('purchase_orders_browser'))

		self.check_get_redirects(urlname=reverse('delete_job'))

	def test_visibility_permissions_manager(self):
		self.loginManager()

		self.check_get_redirects(urlname=reverse('delete_job'))

	def test_deletes_permissions_staff(self):

		job = Jobs.objects.filter(address='200 Park Avenue').first()

		SL_item_query = Shopping_list_items.objects.filter(description='job 1 shopping list item 1')
		SL_item = SL_item_query.first()

		ASL_item_query = Items.objects.filter(description='job 1 acquired shopping list item 1')
		ASL_item = ASL_item_query.first()

		PO_item_query = Items.objects.filter(description='job 1 purchase order 1 item 1 description')
		PO_item = PO_item_query.first()

		job_note_query = Notes.objects.filter(Title='job 1 note 1 title')
		job_note = job_note_query.first()

		admin_note_query = Notes.objects.filter(Title='admin note 1 title')
		admin_note = admin_note_query.first()

		self.loginStaff()

		# delete job
		# tested in front end

		# delete shopping list item
		self.check_get_redirects(reverse('delete', kwargs={'model':'Shopping_list_items', 'pk':SL_item.pk})) # get requests delete things, and when testing it redirects to the homepage (see view function for explanation)
		self.assertTrue(SL_item_query.exists())

		# delete acuired shopping list item
		self.check_get_redirects(reverse('delete', kwargs={'model':'Acquired_Item', 'pk':ASL_item.pk}))
		self.assertTrue(ASL_item_query.exists())

		# delete purchase order item
		self.check_get_redirects(reverse('delete', kwargs={'model':'Items', 'pk':PO_item.pk}))
		self.assertTrue(PO_item_query.exists())

		# delete job note
		self.check_get_redirects(reverse('delete', kwargs={'model':'Notes', 'pk':job_note.pk}))
		self.assertTrue(job_note_query.exists())

		# delete admin note
		self.check_get_redirects(reverse('delete', kwargs={'model':'Notes', 'pk':admin_note.pk}))
		self.assertTrue(admin_note_query.exists())




	def test_deletes_permissions_manager(self):

		job = Jobs.objects.filter(address='200 Park Avenue').first()

		SL_item_query = Shopping_list_items.objects.filter(description='job 1 shopping list item 1')
		SL_item = SL_item_query.first()

		ASL_item_query = Items.objects.filter(description='job 1 acquired shopping list item 1')
		ASL_item = ASL_item_query.first()

		PO_item_query = Items.objects.filter(description='job 1 purchase order 1 item 1 description')
		PO_item = PO_item_query.first()

		job_note_query = Notes.objects.filter(Title='job 1 note 1 title')
		job_note = job_note_query.first()

		admin_note_query = Notes.objects.filter(Title='admin note 1 title')
		admin_note = admin_note_query.first()

		self.loginManager()

		# delete job
		# tested in front end

		# delete shopping list item
		self.check_get_redirects(reverse('delete', kwargs={'model':'Shopping_list_items', 'pk':SL_item.pk})) # get requests delete things, and when testing it redirects to the homepage (see view function for explanation)
		self.assertTrue(SL_item_query.exists())

		# delete acuired shopping list item
		self.check_get_redirects(reverse('delete', kwargs={'model':'Acquired_Item', 'pk':ASL_item.pk}))
		self.assertTrue(ASL_item_query.exists())

		# delete purchase order item
		self.check_get_redirects(reverse('delete', kwargs={'model':'Items', 'pk':PO_item.pk}))
		self.assertTrue(PO_item_query.exists())

		# delete job note
		self.check_get_redirects(reverse('delete', kwargs={'model':'Notes', 'pk':job_note.pk}))
		self.assertTrue(job_note_query.exists())

		# delete admin note
		self.check_get_redirects(reverse('delete', kwargs={'model':'Notes', 'pk':admin_note.pk}))
		self.assertTrue(admin_note_query.exists())











