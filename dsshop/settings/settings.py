"""
Django settings for dsshop project.

Generated by 'django-admin startproject' using Django 1.9.9.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

# Amazon S3 requirements? 
os.environ['S3_USE_SIGV4'] = 'True'
os.environ['SWF'] = 'eu-central-1'

# AMAZON S3 STORAGE
AWS_STORAGE_BUCKET_NAME = 'dsshop'
AWS_REGION = 'eu-central-1'
AWS_S3_HOST = 's3.eu-central-1.amazonaws.com'

AWS_S3_CUSTOM_DOMAIN = '%s.s3.eu-central-1.amazonaws.com' % AWS_STORAGE_BUCKET_NAME


from oscar.defaults import *

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

from django.utils.translation import ugettext_lazy as _

LANGUAGE_CODE = 'nl-be'

LANGUAGES = [
    ('nl', _('Dutch')),
    ('fr', _('French')),
    #('en', _('English')),
]

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

print(LOCALE_PATHS)

#STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '!4e7cfxq_!(8g(*w^f5omk(!ox!z=-nrmh28m2y@ne1$)v=z_k'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

from oscar import get_core_apps

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.flatpages',
    'modeltranslation', # Translation of models (productnamen, categorieen, ...) -> moest voor django.contrib.admin komen
    'django.contrib.admin',

    # DJANGO OSCAR API
    'oscarapi',

    # Third party applications
    'storages',         # Use to connect with Amazon S3
    'compressor',       # static file compression (may be deleted because of Heroku deployment?)
    'widget_tweaks',    # Forms customizations
    #'imageresize',       # Image resizing before upload
    
    'rest_framework',   # Required om gebruik te kunnen maken van oscarapi
    'Crypto',

    'dsshop',


] + get_core_apps(['myapps.catalogue', 'myapps.basket', 'myapps.partner', 
    'myapps.checkout', 'myapps.payment', 'myapps.shipping', 'myapps.dashboard.catalogue'])

SITE_ID = 1


MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'oscar.apps.basket.middleware.BasketMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
]

AUTHENTICATION_BACKENDS = (
    'oscar.apps.customer.auth_backends.EmailBackend',
    'django.contrib.auth.backends.ModelBackend',
)

ROOT_URLCONF = 'dsshop.urls'

from oscar import OSCAR_MAIN_TEMPLATE_DIR

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
            OSCAR_MAIN_TEMPLATE_DIR
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',

                'oscar.apps.search.context_processors.search_form',
                'oscar.apps.promotions.context_processors.promotions',
                'oscar.apps.checkout.context_processors.checkout',
                'oscar.apps.customer.notifications.context_processors.notifications',
                'oscar.core.context_processors.metadata',
            ],
        },
    },
]

WSGI_APPLICATION = 'dsshop.wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/



TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'common_static'),
)

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

FILE_UPLOAD_TEMP_DIR = MEDIA_ROOT

# The below setting is used for file uploads. Any file larger than 10Mb will not be handled in memory
FILE_UPLOAD_MAX_MEMORY_SIZE = 10485760

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
    },
}

#HAYSTACK_CONNECTIONS = {
#    'default': {
#        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
#        'URL': 'http://127.0.0.1:8983/solr',
#        'INCLUDE_SPELLING': True,
#    },
#}

# SHOP SETTINGS
OSCAR_DEFAULT_CURRENCY = 'EUR'
OSCAR_SHOP_NAME = 'Tom Verheyden'

OSCAR_ALLOW_ANON_CHECKOUT = True

# Hidden Oscar features, e.g. wishlists or reviews
OSCAR_HIDDEN_FEATURES = ['reviews', 'wishlists',]

# Menu structure of the dashboard navigation
OSCAR_DASHBOARD_NAVIGATION = [
    {
        'label': _('Dashboard'),
        'icon': 'icon-th-list',
        'url_name': 'dashboard:index',
    },
    {
        'label': _('Catalogue'),
        'icon': 'icon-sitemap',
        'children': [
            {
                'label': _('Products'),
                'url_name': 'dashboard:catalogue-product-list',
            },
            {
                'label': _('Product Types'),
                'url_name': 'dashboard:catalogue-class-list',
            },
            {
                'label': _('Categories'),
                'url_name': 'dashboard:catalogue-category-list',
            },
#            {
#                'label': _('Ranges'),
#                'url_name': 'dashboard:range-list',
#            },
#            {
#                'label': _('Low stock alerts'),
#                'url_name': 'dashboard:stock-alert-list',
#            },
        ]
    },
#    {
#        'label': _('Fulfilment'),
#        'icon': 'icon-shopping-cart',
#        'children': [
#            {
#                'label': _('Orders'),
#                'url_name': 'dashboard:order-list',
#            },
#            {
#                'label': _('Statistics'),
#                'url_name': 'dashboard:order-stats',
#            },
#            {
#                'label': _('Partners'),
#                'url_name': 'dashboard:partner-list',
#            },
            # The shipping method dashboard is disabled by default as it might
            # be confusing. Weight-based shipping methods aren't hooked into
            # the shipping repository by default (as it would make
            # customising the repository slightly more difficult).
            # {
            #     'label': _('Shipping charges'),
            #     'url_name': 'dashboard:shipping-method-list',
            # },
#        ]
#    },
    {
        'label': _('Customers'),
        'icon': 'icon-group',
        'children': [
            {
                'label': _('Customers'),
                'url_name': 'dashboard:users-index',
            },
#            {
#                'label': _('Stock alert requests'),
#                'url_name': 'dashboard:user-alert-list',
#            },
        ]
    },
#    {
#        'label': _('Offers'),
#        'icon': 'icon-bullhorn',
#        'children': [
#            {
#                'label': _('Offers'),
#                'url_name': 'dashboard:offer-list',
#            },
#            {
#                'label': _('Vouchers'),
#                'url_name': 'dashboard:voucher-list',
#            },
#        ],
#    },
#    {
#        'label': _('Content'),
#        'icon': 'icon-folder-close',
#        'children': [
#            {
#                'label': _('Content blocks'),
#                'url_name': 'dashboard:promotion-list',
#            },
#            {
#                'label': _('Content blocks by page'),
#                'url_name': 'dashboard:promotion-list-by-page',
#            },
#            {
#                'label': _('Pages'),
#                'url_name': 'dashboard:page-list',
#            },
#            {
#                'label': _('Email templates'),
#                'url_name': 'dashboard:comms-list',
#            },
#            {
#                'label': _('Reviews'),
#                'url_name': 'dashboard:reviews-list',
#            },
#        ]
#    },
    {
        'label': _('Reports'),
        'icon': 'icon-bar-chart',
        'url_name': 'dashboard:reports-index',
    },
]

OSCAR_PRODUCTS_PER_PAGE = 21
OSCAR_RECENTLY_VIEWED_PRODUCTS = 10
OSCAR_ACCOUNTS_REDIRECT_URL = '/'

OSCAR_INITIAL_ORDER_STATUS = 'Aanvraag'
OSCAR_ORDER_STATUS_PIPELINE = {
    'Aanvraag': ('Verzendkosten toegevoegd', 'afhaling door klant', 'Geannuleerd',),
    'Verzendkosten toegevoegd': ('Betaald', 'Geannuleerd '),
    'Afhaling door klant': ('Betaald','Geannuleerd', ),
    'Betaald': ('Verwerkt'),
    'Verwerkt': (),
    'Geannuleerd': (),
}

DEV = False
