
# AMAZON S3 STORAGE
AWS_STORAGE_BUCKET_NAME = 'dsshop'
AWS_REGION = 'eu-central-1'
AWS_ACCESS_KEY_ID = 'AKIAJMC2L6WZ3TCR4RFQ'
AWS_SECRET_ACCESS_KEY = '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'
AWS_S3_HOST = 's3.eu-central-1.amazonaws.com'

AWS_S3_CUSTOM_DOMAIN = '%s.s3.eu-central-1.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

MEDIAFILES_LOCATION = 'media'
MEDIA_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, MEDIAFILES_LOCATION)
DEFAULT_FILE_STORAGE = 'home.custom_storages.MediaStorage'

# WHITENOISE
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

# DATABASE SETUP
import dj_database_url
DATABASES['default'] =  dj_database_url.config()

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']