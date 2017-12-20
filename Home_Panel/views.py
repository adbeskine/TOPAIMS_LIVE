from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse
import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta

from Item_Flow.models import Items, Purchase_orders
from Notes.models import Notes
from Shopping_list.models import Shopping_list_items

from Item_Flow.forms import reject_delivery_form, purchase_order_form
from Shopping_list.forms import new_shopping_list_item_form
from Notes.forms import new_note_form

#--HELPER METHODS--#

def convert_to_date(str_date, form='%Y-%m-%d'):
	dt = datetime.datetime.strptime(str_date, form)
	return dt.date()

from _Auth.views import check_and_render

#-- VIEWS --#

def homepage(request):  #LOGGEDIN

	NOW = settings.NOW
	
	next_PO_number = Purchase_orders.objects.count() + 4001


	all_delivery_items = []
	this_week_delivery_items = []
	today_delivery_items = []

	for item in Items.objects.filter(status='ORDERED', delivery_location='shop'): #when something is marked as 'in showroom' it doesn't reappear
		
		if item.delivery_date == NOW.strftime('%Y-%m-%d'):
			today_delivery_items.append(item)
			this_week_delivery_items.append(item)
		
		elif convert_to_date(item.delivery_date).isocalendar()[1] == NOW.isocalendar()[1]:
			this_week_delivery_items.append(item)

		elif convert_to_date(item.delivery_date) >= NOW:
			all_delivery_items.append(item)

	admin_notes = []
	job_notes = []
	for note in Notes.objects.all():
		
		if note.job == None:
			admin_notes.append(note)
		
		else:
			job_notes.append(note)

	context = {
	'today_delivery_items':today_delivery_items,
	'this_week_delivery_items':this_week_delivery_items,
	'all_delivery_items':all_delivery_items,
	'reject_delivery_form':reject_delivery_form,

	'shopping_list_items':Shopping_list_items.objects.all(),
	'new_shopping_list_item_form':new_shopping_list_item_form,

	'admin_notes':admin_notes,
	'job_notes':job_notes,
	'new_note_form':new_note_form,

	'purchase_order_form':purchase_order_form,
	'next_PO_number':next_PO_number,
	}


	return check_and_render(request, 'Home_Panel/home.html', context)	

# Create your views here.
