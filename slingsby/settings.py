# coding: utf-8

import os

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = [
    '.ntnuita.no',
]

USE_TZ = True
TIME_ZONE = 'Europe/Oslo'
FIRST_DAY_OF_WEEK = 1 # Søndag = 0, Mandag = 1

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'USER': 'slingsby',
        'NAME': 'slingsby_rel',
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': 'unix:/tmp/memcached.socket',
    }
}

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.staticfiles',

    'slingsby.archive',
    'slingsby.articles',
    'slingsby.auth',
    'slingsby.events',
    'slingsby.gear',
    'slingsby.general',
    'slingsby.musikk',
    'slingsby.quotes',
    'slingsby.tasks',
    'slingsby.users',

    'social_auth',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',

    'slingsby.general.middleware.HttpAcceptMiddleware',
    'slingsby.general.middleware.HttpMethodOverride',
)

SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

AUTHENTICATION_BACKENDS = (
  'social_auth.backends.google.GoogleOAuth2Backend',
  'social_auth.backends.facebook.FacebookBackend',

  'django.contrib.auth.backends.ModelBackend',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'django.core.context_processors.debug',

    'slingsby.general.context_processors.default',
    'slingsby.quotes.context_processors.default',

    'social_auth.context_processors.social_auth_by_name_backends',
    'social_auth.context_processors.social_auth_backends',
    'social_auth.context_processors.social_auth_by_type_backends',
    'social_auth.context_processors.social_auth_login_redirect',
)

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), 'templates'),
)

ROOT_URLCONF = 'slingsby.urls'

STATIC_URL = 'http://org.ntnu.no/telemark/static/'

# social_auth specific settings
SOCIAL_AUTH_DEFAULT_USERNAME = 'new_social_auth_user'
SOCIAL_AUTH_UID_LENGTH = 16
SOCIAL_AUTH_ASSOCIATION_HANDLE_LENGTH = 16
SOCIAL_AUTH_NONCE_SERVER_URL_LENGTH = 16
SOCIAL_AUTH_ASSOCIATION_SERVER_URL_LENGTH = 16
SOCIAL_AUTH_ASSOCIATION_HANDLE_LENGTH = 16
SOCIAL_AUTH_ENABLED_BACKENDS = (
    'facebook',
)
FACEBOOK_APP_ID = '1416174671936188'
FACEBOOK_EXTENDED_PERMISSIONS = ['email']
