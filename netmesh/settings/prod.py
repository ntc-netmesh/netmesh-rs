from .base import *


# Security settings
SECURE_HSTS_SECONDS = 30
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
X_FRAME_OPTIONS = 'DENY'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'netmesh',
        'USER': 'netmesh',
        'PASSWORD': 'netmesh',
        'HOST': 'localhost',
        'PORT': '',
    }
}
