from slingsby.settings import *

SECRET_KEY = '{{ pillar["SECRET_KEY"] }}'

SOCIAL_AUTH_FACEBOOK_SECRET = '{{ pillar["SOCIAL_AUTH_FACEBOOK_SECRET"] }}'

ALLOWED_HOSTS = (
    '.ntnuita.no',

    # localhost needed so that curl can access the /tasks/
    'localhost',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'slingsby_rel',
        'HOST': 'db-slingsby-rel.crj3xomafakq.eu-west-1.rds.amazonaws.com',
        'USER': 'slingsby',
        'PASSWORD': '{{ pillar["MYSQL_PASSWORD"] }}',
    },
}

_static_url_base = 'http://ntnuita.no/static/%s/'

_slingsby_version = '{{ pillar["slingsby_version"] }}'

STATIC_URL = _static_url_base % _slingsby_version
