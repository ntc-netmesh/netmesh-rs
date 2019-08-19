from .base import *

DEBUG = True

INSTALLED_APPS += [
    'django_nose',
]

# Use nose to run all tests
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'