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

STATIC_URL = 'static/'

STATIC_ROOT = path.join(path.dirname(__file__), 'slingsby', 'static')

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda req: DEBUG,
}

DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.version.VersionDebugPanel',
    'debug_toolbar.panels.timer.TimerDebugPanel',
    'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
    'debug_toolbar.panels.headers.HeaderDebugPanel',
    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
    'debug_toolbar.panels.template.TemplateDebugPanel',
    'debug_toolbar.panels.sql.SQLDebugPanel',
    'debug_toolbar.panels.signals.SignalDebugPanel',
    'debug_toolbar.panels.logger.LoggingPanel',
)

MIDDLEWARE_CLASSES = tuple(list(MIDDLEWARE_CLASSES) + [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
])

INSTALLED_APPS = tuple(list(INSTALLED_APPS) + [
    'debug_toolbar',
    'django_nose',
])

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
