from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponse
from django.contrib import messages
from _Auth.views import check_permissions, check_and_render
import re

from Jobs.models import Jobs
from Item_Flow.models import Items, Scheduled_items
from Shopping_list.models import Shopping_list_items
from Notes.models import Notes

from Jobs.forms import new_job_form, delete_job_form


def jobs(request): # LOGGEDIN

	perm_level = request.session['perm_level']

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
	'perm_level':perm_level,
	}

	return check_and_render(request, 'Jobs/jobs.html', context)

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

	if check_permissions(request, 2) == True:
		pass
	else:
		return check_permissions(request, 2)

	return check_and_render(request, 'Jobs/new_job_form.html', {'form':form}) 

def update_job(request, job_id, status): # LOGGEDIN ADMIN
	
	if request.method == 'GET':

		if check_permissions(request, 2) == True:
			pass
		else:
			return check_permissions(request, 2)

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

def delete_job(request):

	if check_permissions(request, 3) == True:
			pass
	else:
		return check_permissions(request, 3)

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
	return check_and_render(request, 'Jobs/delete_job.html', context)