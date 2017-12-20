from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse

from Jobs.models import Jobs
from Notes.models import Notes
from Item_Flow.models import Scheduled_items, Items, Purchase_orders
from Shopping_list.models import Shopping_list_items

from Notes.forms import new_note_form
from Item_Flow.forms import new_scheduled_item_form, update_scheduled_item_date_form, purchase_order_form
from Shopping_list.forms import new_shopping_list_item_form


#-- HELPER METHODS --#

from _Auth.views import check_and_render

#-- VIEWS --#

def job(request, job_id): # LOGGEDIN
	
	NOW = settings.NOW
	perm_level = request.session['perm_level']
	job = Jobs.objects.filter(job_id=job_id).first()
	

	next_PO_number = Purchase_orders.objects.count() + 4001


	#-- NOTES --#
	notes = Notes.objects.filter(job=job).order_by('-Timestamp')

	#-- PROFILE --#
	
	if job.status == 'quote':
		job_colour = 'WHITE_PROFILE_BOX'
	elif job.status == 'ongoing':
		job_colour = 'ULTRAMARINE_BLUE_PROFILE_BOX'
	elif job.status=='completed':
		job_colour = 'FAINT_BLUE_PROFILE_BOX'

	#-- SCHEDULE OF ITEMS --#
	scheduled_items = Scheduled_items.objects.filter(job=job).order_by('date_1')

	#-- SITE MANAGEMENT --#
	
	needed_items = []
	for item in scheduled_items:
		# if item.date_1 - NOW <= timedelta(days=7):
		needed_items.append(item)
	for item in Shopping_list_items.objects.filter(job=job):
		needed_items.append(item)

	en_route_items = []
	for item in Items.objects.filter(job=job, status='ORDERED'): # later add 'arrived' status
		en_route_items.append(item)
	for item in Items.objects.filter(job=job, status='ACQUIRED'):
		en_route_items.append(item)
	for item in Items.objects.filter(job=job, status='IN SHOWROOM'):
		en_route_items.append(item)

	on_site_items = []
	for item in Items.objects.filter(job=job, status='ON-SITE'):
		on_site_items.append(item)

	context = {
		'job':job,
		'profile_colour':job_colour,


		'now':NOW,
		'next_PO_number': next_PO_number,
		'perm_level':perm_level,

		'new_note_form':new_note_form,
		'new_scheduled_item_form':new_scheduled_item_form,
		'update_date_form':update_scheduled_item_date_form,
		'purchase_order_form':purchase_order_form,
		'new_shopping_list_item_form':new_shopping_list_item_form,

		'notes':notes,
		'scheduled_items':scheduled_items,
		'needed_items':needed_items,
		'en_route_items':en_route_items,
		'on_site_items':on_site_items
	}
	
	return check_and_render(request, 'Jobs_Panel/job.html', context)
