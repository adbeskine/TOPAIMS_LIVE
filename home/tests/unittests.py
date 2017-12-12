import os

os.system("echo TEST JOB VIEW")
os.system("python manage.py test home.tests.test_job_view")

os.system("echo TEST JOBS")
os.system("python manage.py test home.tests.test_jobs")

os.system("echo TEST LOGIN")
os.system("python manage.py test home.tests.test_login")

os.system("echo TEST SHOPPING LIST")
os.system("python manage.py test home.tests.test_shopping_list")

os.system("echo TEST HOME PAGE")
os.system("python manage.py test home.tests.test_home_page")

os.system("echo TEST PURCHASE ORDER VIEWS")
os.system("python manage.py test home.tests.test_purchase_order_view")

os.system("echo TEST DELETES")
os.system("python manage.py test home.tests.test_deletes")

# os.system("echo TEST PERMISSIONS")
# os.system("python manage.py test home.tests.test_permissions")