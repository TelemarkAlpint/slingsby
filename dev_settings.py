# pylint: disable=unused-wildcard-import,wildcard-import

# Override settings locally
from slingsby.settings import *
from os import path
import os

DEBUG = True

DEBUG_TOOLBAR = os.environ.get('DJANGO_DEBUG_TOOLBAR', False)

TEMPLATE_DEBUG = DEBUG

SECRET_KEY = 'pleasedontusethisinprod'

SOCIAL_AUTH_FACEBOOK_SECRET = 'pleasedontusethisinprod'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'slingsby_rel.sqlite',
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'slingsby_rel'
    }
}

# Used for the query debugger that's run in dev mode.
INTERNAL_IPS = ("127.0.0.1", "::1")

STATIC_URL = '/static/'

# This is where collectstatic gathers the static files from the installed apps
STATIC_ROOT = path.join(path.dirname(__file__), '.tmp', 'static')

# This is where static files are served from
STATICFILES_DIRS = (
   path.join(path.dirname(__file__), 'build', 'static'),
)

INSTALLED_APPS = list(INSTALLED_APPS) + [
    'django_nose',
]

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

ALLOWED_HOSTS = (
    'localhost',
    'ntnuita.local',
)

if DEBUG_TOOLBAR:
    DEBUG_TOOLBAR_CONFIG = {
        'SHOW_TOOLBAR_CALLBACK': '%s.true' % __name__,
        'SHOW_COLLAPSED': True,
    }

    def true(_):
        return True

    MIDDLEWARE_CLASSES = [
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ] + list(MIDDLEWARE_CLASSES)

    INSTALLED_APPS.append('debug_toolbar')

if os.environ.get('WITH_COVERAGE', False):
    NOSE_ARGS = [
        '--with-coverage',
        '--cover-package=slingsby',
        '--cover-html',
        '--cover-branches',
    ]
