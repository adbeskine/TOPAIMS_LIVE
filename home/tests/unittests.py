import os, winsound

os.system("echo TEST JOB VIEW")
os.system("python manage.py test home.tests.test_job_view")
for i in range(0,10):
	os.system("echo _")
winsound.PlaySound("SystemQuestion", winsound.SND_ALIAS)

os.system("echo TEST JOBS")
os.system("python manage.py test home.tests.test_jobs")
for i in range(0,10):
	os.system("echo _")
winsound.PlaySound("SystemQuestion", winsound.SND_ALIAS)

os.system("echo TEST LOGIN")
os.system("python manage.py test home.tests.test_login")
for i in range(0,10):
	os.system("echo _")
winsound.PlaySound("SystemQuestion", winsound.SND_ALIAS)

os.system("echo TEST SHOPPING LIST")
os.system("python manage.py test home.tests.test_shopping_list")
for i in range(0,10):
	os.system("echo _")
winsound.PlaySound("SystemQuestion", winsound.SND_ALIAS)

os.system("echo TEST HOME PAGE")
os.system("python manage.py test home.tests.test_home_page")
for i in range(0,10):
	os.system("echo _")
winsound.PlaySound("SystemQuestion", winsound.SND_ALIAS)

os.system("echo TEST PURCHASE ORDER VIEWS")
os.system("python manage.py test home.tests.test_purchase_order_view")
for i in range(0,10):
	os.system("echo _")
winsound.PlaySound("SystemQuestion", winsound.SND_ALIAS)

os.system("echo TEST DELETES")
os.system("python manage.py test home.tests.test_deletes")
for i in range(0,10):
	os.system("echo _")
winsound.PlaySound("SystemQuestion", winsound.SND_ALIAS)

os.system("echo TEST PERMISSIONS")
os.system("python manage.py test home.tests.test_permissions")


for i in range(0, 2):
	winsound.PlaySound("SystemQuestion", winsound.SND_ALIAS)