from django.shortcuts import redirect
from django.urls import reverse
from _Auth.views import check_and_render
from Shopping_list.forms import new_shopping_list_item_form
from Item_Flow.models import Items
from Jobs.models import Jobs
from Shopping_list.models import Shopping_list_items



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

	return check_and_render(request, 'Shopping_list/shopping_list.html', context)
