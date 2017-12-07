import os


os.system("echo JOB VIEW TEST")
os.system("python manage.py test functional_tests.test_job_view")


os.system("echo LOGIN TEST")
os.system("python manage.py test functional_tests.test_login")

os.system("echo JOBS TEST")
os.system("python manage.py test functional_tests.test_jobs")

os.system("echo SHOPPING LIST TEST")
os.system("python manage.py test functional_tests.test_shopping_list")

os.system("echo HOME PAGE TEST")
os.system("python manage.py test functional_tests.test_home_page")

os.system("echo PURCHASE ORDER VIEWS TEST")
os.system("python manage.py test functional_tests.test_purchase_order_view")
