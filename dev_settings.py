# pylint: disable=unused-wildcard-import,wildcard-import

# Override settings locally
from slingsby.settings import *
from os import path

DEBUG = True

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

STATIC_ROOT = path.join(path.dirname(__file__), 'build', '.tmp')

STATICFILES_DIRS = (
   path.join(path.dirname(__file__), 'slingsby', 'static'),
)

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': '%s.true' % __name__,
}

def true(_):
    return True

MIDDLEWARE_CLASSES = tuple([
    'debug_toolbar.middleware.DebugToolbarMiddleware',
] + list(MIDDLEWARE_CLASSES))

INSTALLED_APPS = tuple(list(INSTALLED_APPS) + [
    'debug_toolbar',
    'django_nose',
])

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

ALLOWED_HOSTS = (
    'localhost',
    'ntnuita.no',
)
