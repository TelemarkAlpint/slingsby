from slingsby.settings import *

SECRET_KEY = '{{ pillar["SECRET_KEY"] }}'

FACEBOOK_API_KEY = '{{ pillar["FACEBOOK_API_KEY"] }}'

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
