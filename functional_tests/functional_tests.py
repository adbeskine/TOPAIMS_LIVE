import os, winsound


os.system("echo JOB VIEW TEST")
os.system("python manage.py test functional_tests.test_job_view")
for i in range(0,10):
	os.system("echo _")
winsound.PlaySound("SystemQuestion", winsound.SND_ALIAS)



os.system("echo LOGIN TEST")
os.system("python manage.py test functional_tests.test_login")
for i in range(0,10):
	os.system("echo _")
winsound.PlaySound("SystemQuestion", winsound.SND_ALIAS)


os.system("echo JOBS TEST")
os.system("python manage.py test functional_tests.test_jobs")
for i in range(0,10):
	os.system("echo _")
winsound.PlaySound("SystemQuestion", winsound.SND_ALIAS)


os.system("echo SHOPPING LIST TEST")
os.system("python manage.py test functional_tests.test_shopping_list")
for i in range(0,10):
	os.system("echo _")
winsound.PlaySound("SystemQuestion", winsound.SND_ALIAS)


os.system("echo HOME PAGE TEST")
os.system("python manage.py test functional_tests.test_home_page")
for i in range(0,10):
	os.system("echo _")
winsound.PlaySound("SystemQuestion", winsound.SND_ALIAS)


os.system("echo PURCHASE ORDER VIEWS TEST")
os.system("python manage.py test functional_tests.test_purchase_order_view")
for i in range(0,10):
	os.system("echo _")
winsound.PlaySound("SystemQuestion", winsound.SND_ALIAS)


os.system("echo DELETES TEST")
os.system("python manage.py test functional_tests.test_deletes")
for i in range(0,10):
	os.system("echo _")
winsound.PlaySound("SystemQuestion", winsound.SND_ALIAS)


os.system("echo PERMISSIONS TEST")
os.system("python manage.py test functional_tests.test_permissions")


for i in range(0, 2):
	winsound.PlaySound("SystemQuestion", winsound.SND_ALIAS)	

