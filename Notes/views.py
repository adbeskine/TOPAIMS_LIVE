from django.shortcuts import redirect
from django.urls import reverse
from Notes.models import Notes
from Jobs.models import Jobs
from Notes.forms import new_note_form

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