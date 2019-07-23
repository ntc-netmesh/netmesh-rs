from .base import *

DEBUG = True

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.sqlite3',
       'NAME': os.path.join(BASE_DIR, 'netmesh.sqlite3'),
   }
}