from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse
import os, random, string
from _Auth.models import Site_info, Pass

#-- HELPER METHODS --#
def generate_password():
	length = 50
	chars = string.ascii_letters + string.digits
	random.seed = (os.urandom(1024))
	return ''.join(random.choice(chars) for i in range(length))


def check_permissions(request, minimum_level):

	# obtain previous_page value

	if request.META['SERVER_NAME'] == 'testserver':  # this is what happens in the unit tests. The redirect is tested in the FTs
		previous_page = reverse('homepage')
	else:
		try:
			previous_page = request.META['HTTP_REFERER'] # does not exist when unit testing
		except KeyError:
			previous_page = reverse('homepage')

	# check perm level

	if request.session['perm_level'] >= minimum_level:
		perm_level = request.session['perm_level']
		return True
	elif request.session['perm_level'] < minimum_level:
		return redirect(previous_page)

def check_and_render(request, template, context = None):
	try:
		if request.session['logged_in'] == True:
			return render(request, template, context)
		else:
			return redirect(reverse('login'))
	except KeyError:
		return redirect(reverse('login'))


#-- VIEWS --#

def login(request): #
	site = Site_info.objects.first()

	if site.locked == True:
		return render(request, '_Auth/locked.html')
	else:
		pass
	
	if request.method == 'POST':
		
		if site.locked == True: # make sure the website isn't locked (for POST data not through website form) POST_MVP: proper django form, check for csrf token instead
			return redirect(reverse('login'))
		elif site.locked == False:
			pass

		if Pass.objects.filter(password=request.POST.get("password")).exists() == True:
			
			user_object = Pass.objects.filter(password=request.POST.get("password")).first() # remove this line?
			user = user_object.user
			request.session.flush()
			request.session['logged_in'] = True
			# match password with perms and put corresponding perm level as integer in session
			if user == 'staff':
				request.session['perm_level'] = 1
			elif user == 'manager':
				request.session['perm_level'] = 2
			elif user == 'super':
				request.session['perm_level'] = 3


			return redirect(reverse('homepage'))
		
		elif Pass.objects.filter(password=request.POST.get("password")).exists() == False:
	
			try:
				request.session['incorrect_password_attempts'] += 1
			except KeyError:
				request.session['incorrect_password_attempts'] = 0
	
	
			if request.session['incorrect_password_attempts'] < 5: 
				attempts_remaining = (5 - request.session['incorrect_password_attempts'])
				return render(request, '_Auth/login.html', {'password_alert': attempts_remaining}) #  # 
	
			elif request.session['incorrect_password_attempts'] >= 4: # LOCKS THE SITE just in case someone uses creative post requests everything is >= and not ==
				request.session['incorrect_password_attempts'] += 1
					
				Site_info.objects.filter(pk=1).update(locked=True, password=generate_password())				
				return redirect(reverse('login')) # increment the attempts up to five then lock the site

	
	return render(request, '_Auth/login.html')

def unlock(request, unlock_password):
	site = Site_info.objects.first()
	
	if unlock_password == site.password:

		Site_info.objects.filter(pk=1).update(locked=False, password=generate_password())
		del request.session['incorrect_password_attempts']
		return redirect(reverse('login'))
	else:
		return redirect(reverse('login'))

# Create your views here.
