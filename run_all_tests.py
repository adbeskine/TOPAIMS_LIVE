# This will run every test by executing the unit tests file and then the functional tests file. This should be run from the TOPAIMS directory


import os

os.system("python home\\tests\\unittests.py")
os.system("python functional_tests\\functional_tests.py")
