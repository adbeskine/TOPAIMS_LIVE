######################################
######## SYSTEM SETUP GUIDE ##########
######################################

#-- migrate all databases --#
python manage.py migrate
#----                     ----#


#-- set up the site_info --#

# 1
	python manage.py shell # <- run this on the server

# 2
	from home.models import Site_info

	s = Site_info(locked=True, password='firstpasswordshouldchangeeverytimesitelocks')
	s.save()

	exit() # <- this exits the shell
#-----                       -------#

#-- setup passwords --#

# 1
	python manage.py shell

# 2
	from _Auth.models import Pass

	Pass.objects.create(password='staffPassword', user='staff')
	Pass.objects.create(password='managerPassword', user='manager') # <- can view and cru everything, cannot delete anything
	Pass.objects.create(password='superPassword', user='super') # <- has full permissions

