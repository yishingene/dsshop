from .settings import *

DEV = False
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'dsshop_db',                      # Or path to database file if using sqlite3.
        'USER': '',
        'PASSWORD': '',
        'HOST': '',                      # Empty for localhost through domain sockets or           '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}

AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']

MEDIAFILES_LOCATION = 'media'
MEDIA_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, MEDIAFILES_LOCATION)
DEFAULT_FILE_STORAGE = 'dsshop.custom_storages.MediaStorage'

FILE_UPLOAD_TEMP_DIR = MEDIA_ROOT

OSCAR_MISSING_IMAGE_URL = MEDIA_URL + 'image_not_found.jpg'

# WHITENOISE
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

# DATABASE SETUP
import dj_database_url
DATABASES['default'] =  dj_database_url.config()

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Email backend for production
EMAIL_HOST_USER = os.environ['SENDGRID_USERNAME']
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_PASSWORD = os.environ['SENDGRID_PASSWORD']

OSCAR_FROM_EMAIL = 'info@tomverheyden.com'

# Allow these domains
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '.tomverheyden.com', '.aws.amazon.com', '.herokuapp.com']

# Enforce SSL
SECURE_SSL_REDIRECT = True

TEMPLATE_DEBUG = True