from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.contrib import messages
import datetime

from Item_Flow.forms import new_scheduled_item_form, purchase_order_form, update_scheduled_item_date_form, update_PO_supplier_ref_form, reject_delivery_form, update_PO_supplier_ref_form, purchase_order_choice_form
from Jobs.forms import delete_job_form

from Item_Flow.models import Scheduled_items, Purchase_orders, Items
from Shopping_list.models import  Shopping_list_items
from Notes.models import Notes
from Jobs.models import Jobs

from _Auth.views import check_permissions, check_and_render

#-- VIEWS --#


def new_schedule_item(request, job_id):
	
	if request.method == 'POST':

		if check_permissions(request, 2) == True:
			pass
		else:
			return check_permissions(request, 2)

		form = new_scheduled_item_form(request.POST)

		if form.is_valid():
			description = form.cleaned_data['description']
			date_1 = form.cleaned_data['date_1']
			date_2 = form.cleaned_data['date_2']
			quantity = form.cleaned_data['quantity']

			job = Jobs.objects.filter(job_id=job_id).first()

			if date_2 == None:
				date_2 = date_1
				date_1_string = date_1.strftime('%Y/%d/%m')
				new_schedule_item_message = f'"{description}" successfully scheduled for {date_1_string}'

			else:
				date_1_string = date_1.strftime('%Y/%d/%m')
				date_2_string = date_2.strftime('%Y/%d/%m')
				new_schedule_item_message = f'"{description}" successfully scheduled for {date_1_string} - {date_2_string}'

			Scheduled_items.objects.create(
				description = description,
				date_1 = date_1,
				date_2 = date_2,
				quantity = quantity,
				job = job
				)

			messages.add_message(request, messages.INFO, new_schedule_item_message)

			return redirect(reverse('job', kwargs={'job_id':job_id}))

		else:
			print(form.errors)

	else:
		return HttpResponse('how about no?')

def schedule_item(request, function, pk):
	scheduled_item = Scheduled_items.objects.get(pk=pk)
	job = scheduled_item.job

	if request.method == 'POST':
		if check_permissions(request, 2) == True:
			pass
		else:
			return check_permissions(request, 2)
		
		if function == 'update':
			form = update_scheduled_item_date_form(request.POST)

			if form.is_valid():
				scheduled_item.date_1=form.cleaned_data['update_date_1']
				scheduled_item.save()
	
				if form.cleaned_data['update_date_2']:
					scheduled_item.date_2=form.cleaned_data['update_date_2']
					scheduled_item.save()

		elif function == 'delete':
			if check_permissions(request, 3) == True:
				pass
			else:
				return check_permissions(request, 3)
			scheduled_item.delete()

		else:
			return HttpResponse('how about no?')

		return redirect(reverse('job', kwargs={'job_id':job.job_id}))

def purchase_order(request, job_id=None): #SNAGGING, CONDITIONAL VALIDATION

	if request.method == 'POST':

		if check_permissions(request, 2) == True:
			pass
		else:
			return check_permissions(request, 2)

		form = purchase_order_form(request.POST)

		if form.is_valid():

			supplier = form.cleaned_data['Supplier']
			supplier_ref = form.cleaned_data['Supplier_ref']

			new_purchase_order = Purchase_orders.objects.create(supplier=supplier, supplier_ref=supplier_ref)

			for number in range(1, 11):
				if form.cleaned_data[f'item_{number}_description'] != '':

					description = form.cleaned_data[f'item_{number}_description']
					fullname = form.cleaned_data[f'item_{number}_fullname']
					price = form.cleaned_data[f'item_{number}_price']
					job = form.cleaned_data[f'item_{number}_job']
					delivery_location = form.cleaned_data[f'item_{number}_delivery_location']
					delivery_date = form.cleaned_data[f'item_{number}_delivery_date']
					quantity = form.cleaned_data[f'item_{number}_quantity']

					status='ORDERED'
					order_date = settings.NOW
					PO = new_purchase_order
					job = job

					Items.objects.create(
						description = description,
						fullname = fullname,
						delivery_location = delivery_location,
						price = price,
						status = status,
						order_date = order_date,
						delivery_date = delivery_date,
						quantity = quantity,
						PO=PO,
						job=job
						)

				else:
					pass

			if job_id:	
				return redirect(reverse('job', kwargs={'job_id':job_id}))
			else:
				return redirect(reverse('homepage'))
		
		else:
			print(form.errors)

	else:
		return HttpResponse('how about no?')

def update_PO_supplier_ref(request, pk):

	if request.method == 'POST':

		if check_permissions(request, 3) == True:
			pass
		else:
			return check_permissions(request, 3)

	form = update_PO_supplier_ref_form(request.POST)

	if form.is_valid():
		PO = Purchase_orders.objects.filter(pk=pk).first()
		new_ref = form.cleaned_data['new_supplier_ref']
		PO.supplier_ref = new_ref
		PO.save()

		return redirect(reverse('purchase_orders', kwargs={'order_no':PO.id}))

def acquired(request, pk):
	if request.session['logged_in'] == True:
		shopping_list_item = Shopping_list_items.objects.filter(pk=pk).first()
		
		Items.objects.create(
			description = shopping_list_item.description,
			fullname = shopping_list_item.description,
			quantity = shopping_list_item.quantity,
			job = shopping_list_item.job,
			status = 'ACQUIRED',
			delivery_date = settings.NOW,
			model='Acquired_Item'
			)

		messages.add_message(request, messages.INFO, f'{shopping_list_item.description} acquired')
		shopping_list_item.delete()

		return redirect(reverse('shopping_list'))

	else:
		return HttpResponse('how about no?')

def mark_showroom(request, pk):

	if check_permissions(request, 1) == True:
		pass
	else:
		return check_permissions(request, 1)
	item = Items.objects.filter(pk=pk).first()
	item.status='IN SHOWROOM'
	item.save()

	return redirect(reverse('homepage'))

def mark_on_site(request, pk):
	if request.session['logged_in'] == True:
		Item = Items.objects.filter(pk=pk).first()
		job = Item.job

		Item.status='ON-SITE'
		Item.save()

		return redirect(reverse('job', kwargs={'job_id':job.job_id}))

	else:
		return HttpResponse('how about no?')

def reject_delivery(request, pk): # VALIDATION
	if request.method == 'POST':
		if check_permissions(request, 1) == True:
			pass
		else:
			return check_permissions(request, 1)
		form = reject_delivery_form(request.POST)
		item = Items.objects.filter(pk=pk).first()
		job = item.job

		if form.is_valid():

			if form.cleaned_data['reschedule_date']:

				# item has been rescheduled
				note_text = form.cleaned_data['note']
				reschedule_date = form.cleaned_data['reschedule_date']
	
				item.delivery_date = reschedule_date
				item.save()
	
				Notes.objects.create(
					Title = f'ITEM REJECTED - {item.description}',
					Text = f'{note_text} || rescheduled for delivery on {reschedule_date}',
					job = job
					)

				messages.add_message(request, messages.INFO, f'{item.description} rejected')
	
				return redirect(reverse('homepage'))

			elif form.cleaned_data['reschedule_date'] == None:
				
				# item is totally cancelled
				note_text = form.cleaned_data['note']
				item.delete()

				Notes.objects.create(
					Title = f'ITEM REJECTED - {item.description}',
					Text = f'{note_text} || NOT RESCHEDULED',
					job=job
					)

				messages.add_message(request, messages.INFO, f'{item.description} rejected')

				return redirect(reverse('homepage'))


		else:
			print(form.errors)

def delete(request, model=None, pk=None):

	if request.session['logged_in'] == True:

		if check_permissions(request, 3) == True:
			pass
		else:
			return check_permissions(request, 3)

		if request.META['SERVER_NAME'] == 'testserver':
			previous_page = reverse('homepage') # this is what happens in the unit tests. The redirect is tested in the FTs
		else:
			previous_page = request.META['HTTP_REFERER'] # does note exist when unit testing

		if model and pk:

			if model == 'Shopping_list_items':
				item = Shopping_list_items.objects.filter(pk=pk).first()
				item.delete()
	
			elif model == 'Acquired_Item':
				item = Items.objects.filter(pk=pk).first()
				item.delete()
	
			elif model == 'Items':
				item = Items.objects.filter(pk=pk).first()
				item.delete()
	
			elif model == 'Notes':
				item = Notes.objects.filter(pk=pk).first()
				item.delete()

			return redirect(previous_page)

	return redirect(reverse('homepage')) # this is the redirect for all the non-job object deletions

def purchase_orders(request, order_no=None):

	if order_no:

		purchase_order = Purchase_orders.objects.filter(id=order_no).first()
		purchase_order_no = purchase_order.id+4000

		item_list = []
		for item in Items.objects.filter(PO=purchase_order):
			item_list.append(item)

		context = {
			'purchase_order':purchase_order,
			'item_list':item_list,
			'purchase_order_no':purchase_order_no,
			'update_PO_supplier_ref_form':update_PO_supplier_ref_form
		}

		if check_permissions(request, 2) == True:
			pass
		else:
			return check_permissions(request, 2)

		return check_and_render(request, 'Item_Flow/purchase_order.html', context)

	
	if request.method == 'POST':
		form = purchase_order_choice_form(request.POST)
		if form.is_valid():
			purchase_order = form.cleaned_data['purchase_order_number']

			return redirect(reverse('purchase_orders', kwargs={'order_no':purchase_order.id}))

	
	context = {
		'purchase_order_choice_form':purchase_order_choice_form
	}

	if check_permissions(request, 2) == True:
		pass
	else:
		return check_permissions(request, 2)

	return check_and_render(request, 'Item_Flow/purchase_orders.html', context)