from .base import Test
from django.urls import reverse
from datetime import date
from dateutil.relativedelta import relativedelta

from Jobs.forms import new_job_form

from Notes.models import Notes
from Jobs.models import Jobs
from Item_Flow.models import Items
from _Auth.models import Site_info


now = date(year=2017, month=1, day=2) #so tests don't screw up when run on different days of the week make sure that now = a monday
later_this_week = now+relativedelta(days=2)
next_week = now+relativedelta(weeks=1)
two_weeks = now+relativedelta(weeks=2)


class HomePageTests(Test):

	#-- HELPER METHODS --#
	def create_job(self):
		form_data = {
		'Name':'Tony Stark',
		'Email':'Tony@StarkIndustries.net',
		'Phone':'01234567899',
		'Address':'200 Park Avenue',
		'Note':"don't ignore JARVIS, he's temperemental and finds it rude",
		}

		response = self.client.post(reverse('new_job_form'), form_data, follow=True)

	def create_custom_job(self, name, email, phone, address, note):
		form_data = {
		'Name':name,
		'Email':email,
		'Phone':phone,
		'Address':address,
		'Note':note,
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

	#-- SETUP AND TEARDOWN --#

	def setUp(self):
		self.setup_system()
		self.login()
		self.create_job()
		self.create_purchase_order_item('today 1', 'today fname 1', now, job=Jobs.objects.filter(job_id='200ParkAvenue').first())
		self.create_purchase_order_item('today 2', 'today fname 2', now, job=Jobs.objects.filter(job_id='200ParkAvenue').first())
		self.create_purchase_order_item('today 3', 'today fname 3', now, job=Jobs.objects.filter(job_id='200ParkAvenue').first())
		self.create_purchase_order_item('thisweek 1', 'thisweek fname 1', now+relativedelta(days=2), job=Jobs.objects.filter(job_id='200ParkAvenue').first())
		self.create_purchase_order_item('nextweek 1', 'nextweek fname 1', now+relativedelta(weeks=2), job=Jobs.objects.filter(job_id='200ParkAvenue').first())

	#-------------------------------------------------------#
	
	def test_delivered_items_update_statuses(self):

		# correct item - mark showroom
		correct_arrived_item = Items.objects.filter(description='today 1').first()

		self.client.get(reverse('mark_showroom', kwargs={'pk':correct_arrived_item.pk}))
		
		correct_arrived_item = Items.objects.filter(description='today 1').first()
		self.assertEquals(correct_arrived_item.status, 'IN SHOWROOM')

		# reject and reschedule item
		reject_and_reschedule_item = Items.objects.filter(description='today 2').first()
		reject_and_reschedule_form_data = {
			'reschedule_date' : later_this_week,
			'note':'item damaged',
			}
		notes_count = Notes.objects.count() # REFRACT look at how this makes sure that a new note is correctly added, there HAS to be a neater way to do this

		self.client.post(reverse('reject_delivery', kwargs={'pk':reject_and_reschedule_item.pk}), data=reject_and_reschedule_form_data, follow=True)

		reject_and_reschedule_item = Items.objects.filter(description='today 2').first()
		self.assertEquals(reject_and_reschedule_item.status, 'ORDERED')
		self.assertEquals(reject_and_reschedule_item.delivery_date, later_this_week.strftime('%Y-%m-%d')) # not sure how it is rendered in the model, may need to adjust equality parameters
		self.assertEquals(Notes.objects.count(), notes_count+1)
		latest_note = Notes.objects.filter(pk=notes_count+1).first()
		self.assertEquals(latest_note.job, reject_and_reschedule_item.job)
		self.assertEquals(latest_note.Title, 'ITEM REJECTED - today 2')
		self.assertEquals(latest_note.Text, f'item damaged || rescheduled for delivery on {later_this_week}') # maybe adjust how this renders

		# reject and totally cancel item
		reject_and_cancel_item = Items.objects.filter(description='today 3').first()
		reject_and_cancel_item_form_data = {
			'note':'totally wrong item' 
			} # if there is no reschedule date it skips into totally cancelling
		notes_count = Notes.objects.count()

		self.client.post(reverse('reject_delivery', kwargs={'pk':reject_and_cancel_item.pk}), data=reject_and_cancel_item_form_data, follow=True)

		self.assertFalse(Items.objects.filter(pk=reject_and_cancel_item.pk).exists())
		self.assertEquals(Notes.objects.count(), notes_count+1)
		latest_note = Notes.objects.filter(pk=notes_count+1).first()
		self.assertEquals(latest_note.job, reject_and_cancel_item.job)
		self.assertEquals(latest_note.Title, 'ITEM REJECTED - today 3')
		self.assertEquals(latest_note.Text, f'totally wrong item || NOT RESCHEDULED')

	def test_admin_notes(self):
		new_note_data = {
		'Title':'Test admin note',
		'Text':'Hopefully because this will be posted with a job_id of "admin" it will automatically have no job foreignkey and hence can be easily rendered on the homepage admin section'
		}
		
		self.client.post(reverse('new_note', kwargs={'job_id':'admin'}), data=new_note_data, follow=True)

		self.assertTrue(Notes.objects.filter(Title='Test admin note').exists())

		admin_note = Notes.objects.filter(Title='Test admin note').first()
		self.assertEquals(admin_note.job, None)







