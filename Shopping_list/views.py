from django.shortcuts import redirect
from django.urls import reverse
from _Auth.views import check_and_render
from Shopping_list.forms import new_shopping_list_item_form
from Item_Flow.models import Items
from Jobs.models import Jobs
from Shopping_list.models import Shopping_list_items



def shopping_list(request, function=None): #acquired will post to pk link

	# there are only two places where the shopping list form is visible to the user, in the shopping list page or on the homepage.
	# This function handles the shopping list page as well as the creation of new shopping list items from both the home page's form and the shopping list page's form.
	# NOTE - this breaks SRP, needs refracting.

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
		elif function == 'create_homepage': # seperated here so that it redirects back to home page
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
