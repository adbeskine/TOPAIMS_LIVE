from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.contrib import messages
from sensitive import WEBSITE_PASSWORD as password
from .models import Site_info, Jobs, Notes, Scheduled_items, Items, Purchase_orders, Shopping_list_items
import os, random, string, re
from home.forms import delete_job_form, new_job_form, new_note_form, new_scheduled_item_form, update_scheduled_item_date_form, purchase_order_form, purchase_order_choice_form, new_shopping_list_item_form, reject_delivery_form
import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta


# Create your views here.

#--HELPER METHODS--#

def generate_password():
	length = 50
	chars = string.ascii_letters + string.digits
	random.seed = (os.urandom(1024))
	return ''.join(random.choice(chars) for i in range(length))

def check_and_render(request, template, context = None):
	try:
		if request.session['logged_in'] == True:
			return render(request, template, context)
		else:
			return redirect(reverse('login'))
	except KeyError:
		return redirect(reverse('login'))

def convert_to_date(str_date, form='%Y-%m-%d'):
	dt = datetime.datetime.strptime(str_date, form)
	return dt.date()
#-- VIEWS --#



def homepage(request):  #LOGGEDIN

	NOW = settings.NOW


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
	}


	return check_and_render(request, 'home/home.html', context)	


def login(request): #
	site = Site_info.objects.first()

	if site.locked == True:
		return render(request, 'home/locked.html')
	else:
		pass
	
	if request.method == 'POST':
		
		if site.locked == True: # make sure the website isn't locked (for POST data not through website form) POST_MVP: proper django form, check for csrf token instead
			return redirect(reverse('login'))
		elif site.locked == False:
			pass
		
		if request.POST.get("password") == password:
			request.session['logged_in'] = True
			return redirect(reverse('homepage'))
		
		else:
			try:
				request.session['incorrect_password_attempts'] += 1
			except KeyError:
				request.session['incorrect_password_attempts'] = 0


			if request.session['incorrect_password_attempts'] < 5: 
				attempts_remaining = (5 - request.session['incorrect_password_attempts'])
				return render(request, 'home/login.html', {'password_alert': attempts_remaining}) #  # 

			elif request.session['incorrect_password_attempts'] >= 4: # LOCKS THE SITE just in case someone uses creative post requests everything is >= and not ==
				request.session['incorrect_password_attempts'] += 1
				
				Site_info.objects.filter(pk=1).update(locked=True, password=generate_password())				
				return redirect(reverse('login')) # increment the attempts up to five then lock the site

	
	return render(request, 'home/login.html')

def unlock(request, unlock_password):
	site = Site_info.objects.first()
	
	if unlock_password == site.password:

		Site_info.objects.filter(pk=1).update(locked=False, password=generate_password())
		del request.session['incorrect_password_attempts']
		return redirect(reverse('login'))
	else:
		return redirect(reverse('login'))

def new_job(request): # LOGGEDIN, ADMIN

	form = new_job_form

	if request.method == 'POST':

		form = new_job_form(request.POST)

		if form.is_valid():
			Name = form.cleaned_data['Name']
			Email = form.cleaned_data['Email']
			Phone = form.cleaned_data['Phone']
			Address = form.cleaned_data['Address']
			Note = form.cleaned_data['Note']

			job_id = re.sub('\s+', '', Address)

			job = Jobs.objects.create(
				name = Name,
				email = Email,
				phone = Phone,
				address = Address,
				job_id = job_id
				)

			Notes.objects.create(
				Title = 'First Note',
				Text = Note,
				job = job
				)


			return redirect(reverse('job', kwargs={'job_id':job_id}))

	return check_and_render(request, 'home/new_job_form.html', {'form':form}) 

def jobs(request): # LOGGEDIN

	ongoing_jobs = []
	for job in Jobs.objects.filter(status='ongoing'):
		ongoing_jobs.append(job)
	
	completed_jobs = []
	for job in Jobs.objects.filter(status='completed'):
		completed_jobs.append(job)
	
	quote_jobs = []
	for job in Jobs.objects.filter(status='quote'):
		quote_jobs.append(job)

	context = {
	'ongoing_jobs':ongoing_jobs,
	'completed_jobs':completed_jobs,
	'quote_jobs':quote_jobs,
	}

	return check_and_render(request, 'home/jobs.html', context)

def job(request, job_id): # LOGGEDIN
	
	NOW = settings.NOW

	job = Jobs.objects.filter(job_id=job_id).first()

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
		if item.date_1 - NOW <= timedelta(days=7):
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
	
	return check_and_render(request, 'home/job.html', context)


def shopping_list(request, function=None): #acquired will post to pk link

	if request.method == 'POST':
		if function == 'create':

			form = new_shopping_list_item_form(request.POST)
			if form.is_valid():
				description = form.cleaned_data['description']
				quantity = form.cleaned_data['quantity']
				job = form.cleaned_data['job']

				Shopping_list_items.objects.create(
					description = description,
					quantity = quantity,
					job = job
					)
		elif function == 'create_homepage':
			form = new_shopping_list_item_form(request.POST)
			if form.is_valid():
				description = form.cleaned_data['description']
				quantity = form.cleaned_data['quantity']
				job = form.cleaned_data['job']

				Shopping_list_items.objects.create(
					description = description,
					quantity = quantity,
					job = job
					)
			return redirect(reverse('homepage'))

	context = {
		'new_shopping_list_item_form':new_shopping_list_item_form,
		'shopping_list_items':Shopping_list_items.objects.all(),
	}

	return check_and_render(request, 'home/shopping_list.html', context)

def purchase_orders(request, order_no=None):

	if order_no:

		purchase_order = Purchase_orders.objects.filter(order_no=order_no).first()
		purchase_order_no = purchase_order.order_no+4000

		item_list = []
		for item in Items.objects.filter(PO=purchase_order):
			item_list.append(item)

		context = {
			'purchase_order':purchase_order,
			'item_list':item_list,
			'purchase_order_no':purchase_order_no
		}
		return check_and_render(request, 'home/purchase_order.html', context)

	
	if request.method == 'POST':
		form = purchase_order_choice_form(request.POST)
		if form.is_valid():
			purchase_order = form.cleaned_data['purchase_order_number']

			return redirect(reverse('purchase_orders', kwargs={'order_no':purchase_order.order_no}))

	context = {
		'purchase_order_choice_form':purchase_order_choice_form
	}

	return check_and_render(request, 'home/purchase_orders.html', context)

#############################################################
#############################################################
##                   CRUD                                  ##
#############################################################
#############################################################

def new_note(request, job_id): # LOGGEDIN ADMIN

	if request.method == 'POST':

		form = new_note_form(request.POST)

		if form.is_valid():

			if job_id == 'admin':

				Title = form.cleaned_data['Title']
				Text = form.cleaned_data['Text']
	
				new_note = Notes.objects.create(
					Title = Title,
					Text = Text
					)
				return redirect(reverse('homepage'))


			else:

				Title = form.cleaned_data['Title']
				Text = form.cleaned_data['Text']
	
				new_note = Notes.objects.create(
					Title = Title,
					Text = Text,
					job = Jobs.objects.filter(job_id=job_id).first(),
					)
				return redirect(reverse('job', kwargs={'job_id': job_id}))
		else:
			print(form.errors)

def update_job(request, job_id, status): # LOGGEDIN ADMIN
	
	if request.method == 'GET':

		job = Jobs.objects.get(job_id=job_id)

		if status == 'ongoing':
			job.status=status
			job.save()
			return redirect(reverse('job', kwargs={'job_id':job.job_id}))

		elif status == 'completed':
			job.status = status
			job.save()
			return redirect(reverse('job', kwargs={'job_id':job.job_id}))

		elif status == 'quote':
			job.status = status
			job.save()
			return redirect(reverse('job', kwargs={'job_id':job.job_id}))

		else:
			return HttpResponse('How about no?')




#-- ITEM FLOW --#

#-- create items --#

def new_schedule_item(request, job_id):
	
	if request.method == 'POST':
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

def purchase_order(request, job_id=None): #SNAGGING, CONDITIONAL VALIDATION

	if request.method == 'POST':
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

# shopping list item create is above in 'shopping_list'

# -- update items --#

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

def schedule_item(request, function, pk):
	scheduled_item = Scheduled_items.objects.get(pk=pk)
	job = scheduled_item.job

	if request.method == 'POST':
		
		if function == 'update':
			form = update_scheduled_item_date_form(request.POST)

			if form.is_valid():
				scheduled_item.date_1=form.cleaned_data['update_date_1']
				scheduled_item.save()
	
				if form.cleaned_data['update_date_2']:
					scheduled_item.date_2=form.cleaned_data['update_date_2']
					scheduled_item.save()

		elif function == 'delete':
			scheduled_item.delete()

		else:
			return HttpResponse('how about no?')

		return redirect(reverse('job', kwargs={'job_id':job.job_id}))

# -- delete items --#

# schedule item delete in main schedule item method


def delete(request, model=None, pk=None):

	if request.session['logged_in'] == True:

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

		elif model==None and pk==None:

			context = {
				'delete_job_form':delete_job_form
			}

			if request.method == 'POST':

				form = delete_job_form(request.POST)

				if form.is_valid():
					delete_job_address = form.cleaned_data['job_deletion_selection']
					security_field_1 = form.cleaned_data['security_field_1']
					security_field_2 = form.cleaned_data['security_field_2']

					if str(delete_job_address) == str(security_field_1) == str(security_field_2):
						job = Jobs.objects.filter(address=delete_job_address).first()

						Shopping_list_items_to_delete = Shopping_list_items.objects.filter(job=job)
						Acquired_items_to_delete = Items.objects.filter(job=job).filter(status='ACQUIRED')
						Notes_to_delete = Notes.objects.filter(job=job)
						Schedule_items_to_delete = Scheduled_items.objects.filter(job=job)
	
						for item in Shopping_list_items_to_delete:
							item.delete()
						for item in Acquired_items_to_delete:
							item.delete()
						for item in Notes_to_delete:
							item.delete()
						for item in Schedule_items_to_delete:
							item.delete()

						Purchase_order_items_left = Items.objects.filter(job=job)
						for item in Purchase_order_items_left:
							item.job=None
							item.description = f'{item.description} --> {job.address}'
							item.save()

						job.delete()

						messages.add_message(request, messages.INFO, f'{job.address} JOB DELETED')

						return redirect(reverse('homepage'))

					else:
						messages.add_message(request, messages.INFO, 'security fields did not match, nothing deleted')
						return redirect(reverse('delete_job'))
				else:
					print(form.errors) # for test debugging

			return check_and_render(request, 'home/delete_job.html', context)

	return redirect(reverse('homepage')) # this is the redirect for all the non-job object deletions

