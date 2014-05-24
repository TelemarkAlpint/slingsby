from slingsby.settings import *

SECRET_KEY = '{{ pillar["SECRET_KEY"] }}'

SOCIAL_AUTH_FACEBOOK_SECRET = '{{ pillar["SOCIAL_AUTH_FACEBOOK_SECRET"] }}'

ALLOWED_HOSTS = (
    '.ntnuita.no',

    # localhost needed so that curl can access /tasks/
    'localhost',
    {% if grains['id'] == 'vagrant' -%}
    '.ntnuita.local',
    {%- endif %}
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'slingsby_rel',
        'HOST': '{{ pillar['env']['db_uri'] }}',
        'USER': 'slingsby',
        'PASSWORD': '{{ pillar["MYSQL_PASSWORD"] }}',
    },
}

STATIC_URL = '/static/'
