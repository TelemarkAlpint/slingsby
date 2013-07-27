# coding: utf-8

import os

prod_server = os.environ.get('SERVER_SOFTWARE', '').startswith('Google')

if prod_server:
    from .secrets import SECRET_KEY
else:
    SECRET_KEY = 'pleasedontusethisinprod'

USE_TZ = True
TIME_ZONE = 'Europe/Oslo'
FIRST_DAY_OF_WEEK = 1 # Søndag = 0, Mandag = 1

if prod_server:
    DATABASES = {
        'default': {
            'ENGINE': 'google.appengine.ext.django.backends.rdbms',
            'INSTANCE': 'ntnuitelemarkalpint:slingsby-db',
            'NAME': 'slingsby_rel',
        },
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'USER': 'root',
            'HOST': 'localhost',
            'NAME': 'dev_db',
        },
    }
AUTOLOAD_SITECONF = 'indexes'

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.staticfiles',

    'slingsby.articles',
    'slingsby.events',
    'slingsby.quotes',
    'slingsby.musikk',
    'slingsby.tasks',
    'slingsby.upload',
    'slingsby.general',
    'slingsby.archive',
    'slingsby.users',
    'slingsby.gear',

    'debug_toolbar',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'slingsby.general.middleware.HttpAcceptMiddleware',
    'slingsby.general.middleware.CachedAuthMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'

LOGIN_URL = 'http://ntnui.no/authapi/telemark'
LOGIN_REDIRECT_URL = '/'

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'django.core.context_processors.debug',
    'slingsby.general.context_processors.default',
    'slingsby.quotes.context_processors.default',
)

# Used for the query debugger that's run in dev mode.
INTERNAL_IPS = ("127.0.0.1", "::1")

# This test runner captures stdout and associates tracebacks with their
# corresponding output. Helps a lot with print-debugging.
TEST_RUNNER = 'djangotoolbox.test.CapturingTestSuiteRunner'

DEBUG = False
TEMPLATE_DEBUG = False

if not prod_server:
    DEBUG = True
    TEMPLATE_DEBUG = True

TEMPLATE_DIRS = (os.path.join(os.path.dirname(__file__), 'templates'))

ROOT_URLCONF = 'slingsby.urls'

if DEBUG:
    STATIC_URL = '/static/'
else:
    STATIC_URL = 'http://org.ntnu.no/telemark/static/'

AUTH_PROFILE_MODULE = 'slingsby.users.UserProfile'

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
