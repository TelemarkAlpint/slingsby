# coding: utf-8

# Initialize App Engine and import the default settings (DB backend, etc.).
# If you want to use a different backend you have to remove all occurences
# of "djangoappengine" from this file.
from djangoappengine.settings_base import DATABASES
from secrets import SECRET_KEY
import os

USE_TZ = True
TIME_ZONE = 'Europe/Oslo'
FIRST_DAY_OF_WEEK = 1 # Søndag = 0, Mandag = 1

# Activate django-dbindexer for the default database
DATABASES['native'] = DATABASES['default']
DATABASES['default'] = {'ENGINE': 'dbindexer', 'TARGET': 'native'}
AUTOLOAD_SITECONF = 'indexes'

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sessions',
    'djangotoolbox',
    'permission_backend_nonrel',
    'autoload',
    'dbindexer',
    'articles',
    'events',
    'quotes',
    'musikk',
    'tasks',
    'upload',
    'general',
    'archive',
    'users',
    'gear',
    'docutils',
    'pytz',
    'sorl.thumbnail',

    # djangoappengine should come last, so it can override a few manage.py commands
    'djangoappengine',
)

AUTHENTICATION_BACKENDS = (
    'permission_backend_nonrel.backends.NonrelPermissionBackend',
)

MIDDLEWARE_CLASSES = (
    # This loads the index definitions, so it has to come first
    'autoload.middleware.AutoloadMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'general.middleware.HttpAcceptMiddleware',
)

LOGIN_URL = 'http://ntnui.no/authapi/telemark'
LOGIN_REDIRECT_URL = '/'

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'django.core.context_processors.debug',
    'general.context_processors.default',
)

# Used for the query debugger that's run in dev mode.
INTERNAL_IPS = ("127.0.0.1",)

# This test runner captures stdout and associates tracebacks with their
# corresponding output. Helps a lot with print-debugging.
TEST_RUNNER = 'djangotoolbox.test.CapturingTestSuiteRunner'

DEBUG = False
TEMPLATE_DEBUG = False
if os.environ.get('SERVER_SOFTWARE', '').startswith('Dev'):
    DEBUG = True
    TEMPLATE_DEBUG = True

ADMIN_MEDIA_PREFIX =  'http://org.ntnu.no/telemark/static/admin/media/'
TEMPLATE_DIRS = (os.path.join(os.path.dirname(__file__), 'templates'),)

ROOT_URLCONF = 'urls'

STATIC_URL = 'http://org.ntnu.no/telemark/static/'

AUTH_PROFILE_MODULE = 'users.UserProfile'