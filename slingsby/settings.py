# coding: utf-8

from __future__ import print_function

from .celery import app as celery_app # pylint: disable=unused-import

from django.core.urlresolvers import reverse_lazy

import os
import yaml
import json

DEBUG = False

ADMINS = (
    ('NTNUI TA Webmasters', 'telemark-webmaster@ntnui.no'),
    ('Tarjei Husøy', 'apps-telemarkwebmaster@thusoy.com'),
    ('Anders Lysne', 'lysne@live.no')
)

USE_TZ = True

SERVER_EMAIL = 'noreply@ntnuita.no'

DEFAULT_FROM_EMAIL = SERVER_EMAIL

LANGUAGE_CODE = 'nb-NO'

TIME_ZONE = 'Europe/Oslo'

APPEND_SLASH = False

FIRST_DAY_OF_WEEK = 1 # Søndag = 0, Mandag = 1

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'slingsby_rel.sqlite',
    }
}

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.staticfiles',

    'slingsby.archive',
    'slingsby.articles',
    'slingsby.events',
    'slingsby.gear',
    'slingsby.general',
    'slingsby.instagram',
    'slingsby.musikk',
    'slingsby.quotes',
    'slingsby.users',

    # Most of the functionality of django-celery has been merged into celery itself, but the admin
    # interface remains, which is why we need it. This allows us to configure periodic tasks from
    # the admin page.
    'djcelery',
    'social.apps.django_app.default',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',

    'slingsby.general.middleware.HttpAcceptMiddleware',
    'slingsby.general.middleware.HttpMethodOverride',
    'slingsby.general.middleware.ProfileMiddleware',
)

SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

AUTHENTICATION_BACKENDS = (
  'social.backends.facebook.FacebookOAuth2',

  'django.contrib.auth.backends.ModelBackend',
)

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [os.path.join(os.path.dirname(__file__), 'templates')],
    'OPTIONS': {
        'loaders': [
            ('django.template.loaders.cached.Loader', [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ])
        ],
        'context_processors': (
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
            'django.core.context_processors.request',
            'django.core.context_processors.media',
            'django.core.context_processors.debug',

            'slingsby.general.context_processors.default',
            'slingsby.general.context_processors.slingsby_urls',
            'slingsby.general.context_processors.slingsby_config',
            'slingsby.quotes.context_processors.default',

            'social.apps.django_app.context_processors.backends',
            'social.apps.django_app.context_processors.login_redirect',
        ),
        'debug': DEBUG
    }
}]

LOGIN_URL = reverse_lazy('social:begin', kwargs={'backend': 'facebook'})

ROOT_URLCONF = 'slingsby.urls'

EMAIL_SUBJECT_PREFIX = '[ntnuita.no] '

FILE_UPLOAD_PERMISSIONS = 0664

def fix_nonexistent_file_handlers(log_config):
    # If the target log directory doesn't exists, log to current
    # directory. This ensures you don't need /var/log/slingsby to
    # run the devserver, but will still give you the log
    for handler_config in log_config['handlers'].values():
        if 'filename' in handler_config:
            if not os.path.exists(os.path.dirname(handler_config['filename'])):
                handler_config['filename'] = 'log.log'

_log_config_path = os.path.join(os.path.dirname(__file__), 'log_conf.yaml')
with open(_log_config_path) as log_conf_file:
    _log_conf = yaml.load(log_conf_file)
    fix_nonexistent_file_handlers(_log_conf)
    LOGGING = _log_conf


########################################
### python-social-auth specific settings
########################################

SOCIAL_AUTH_DEFAULT_USERNAME = 'new_social_auth_user'

SOCIAL_AUTH_TRAILING_SLASH = False

SOCIAL_AUTH_UID_LENGTH = 16

SOCIAL_AUTH_ASSOCIATION_HANDLE_LENGTH = 16

SOCIAL_AUTH_NONCE_SERVER_URL_LENGTH = 16

SOCIAL_AUTH_ASSOCIATION_SERVER_URL_LENGTH = 16

SOCIAL_AUTH_ASSOCIATION_HANDLE_LENGTH = 16

SOCIAL_AUTH_ENABLED_BACKENDS = (
    'facebook',
)

SOCIAL_AUTH_FACEBOOK_KEY = '1416174671936188'

SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']


#######################################
### Celery settings
#######################################

CELERY_ACCEPT_CONTENT = ['json']

CELERY_TASK_SERIALIZER = 'json'

CELERY_RESULT_SERIALIZER = 'json'


#######################################
#### Settings defined only for slingsby
#######################################

MEDIA_URL = 'http://org.ntnu.no/telemark/media/'

DEFAULT_TITLE = 'NTNUI Telemark-Alpint'

DISQUS_IDENTIFIER = 'telemarkalpint'

INSTAGRAM_CLIENT_ID = 'af9bbc4edab54395ac08747d27ee3295'

_filerevs_path = os.path.join(os.path.dirname(__file__), 'server-assets', 'filerevs.json')
try:
    with open(_filerevs_path) as filerevs_fh:
        FILEREVS = json.load(filerevs_fh)
except IOError:
    print('No file revisions found, continuing without')
    FILEREVS = {}
