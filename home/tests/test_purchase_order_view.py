from .base import Test
from django.urls import reverse
from django.conf import settings
from home.models import Site_info, Items, Purchase_orders, Jobs

class PurchaseOrderViewTest(Test):
	
	#- HELPER METHODS -#
	def create_job(self):
		form_data = {
		'Name':'Tony Stark',
		'Email':'Tony@StarkIndustries.net',
		'Phone':'01234567899',
		'Address':'200 Park Avenue',
		'Note':"don't ignore JARVIS, he's temperemental and finds it rude",
		}

		response = self.client.post(reverse('new_job_form'), form_data, follow=True)

	def create_purchase_order_item(self, description, fullname, delivery_date, Supplier='Stark Industries', Supplier_ref='123', quantity=1, price=1, job=Jobs.objects.first(), delivery_location='shop'):
		PO_data = {
		'Supplier':Supplier,
		'Supplier_ref':Supplier_ref,
		'item_1_description':description,
		'item_1_fullname':fullname,
		'item_1_delivery_location':(delivery_location,),
		'item_1_job':job.address,
		'item_1_delivery_date':delivery_date, #must be date object.
		'item_1_quantity':quantity,
		'item_1_price':price
		}

		self.client.post(reverse('purchase_order', kwargs={'job_id':job.job_id}), data=PO_data, follow=True)

	#- SETUP AND TEARDOWN -#

	def setUp(self):
		now = settings.NOW
		Site_info.objects.create(locked=False, password='thischangesautomaticallyaftereverylock')
		self.login()
		self.create_job()
		self.create_purchase_order_item('testitem1 desc', 'testitem1 fullname', now, job=Jobs.objects.filter(job_id='200ParkAvenue').first())

	#--------------------------------#

	def test_purchase_orders_view(self):
		# this is where the user can browser all the different po numbers
		response = self.client.get(reverse('purchase_orders_browser'))

		self.assertTemplateUsed(response, 'home/purchase_orders.html')

	def test_specific_purchase_order_view(self):
		item = Items.objects.filter(description='testitem1 desc').first()
		
		response = self.client.get(reverse('purchase_orders', kwargs={'order_no':item.PO.order_no}))

		self.assertTemplateUsed(response, 'home/purchase_order.html')
