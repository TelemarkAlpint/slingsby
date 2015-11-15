{% set slingsby = pillar.get('slingsby', {}) -%}

from slingsby.settings import *

import django
import pkg_resources

SECRET_KEY = '{{ slingsby.secret_key }}'

SOCIAL_AUTH_FACEBOOK_SECRET = '{{ pillar.get("SOCIAL_AUTH_FACEBOOK_SECRET", 'youneedmorefootodothis') }}'

ALLOWED_HOSTS = (
    '{{ slingsby.get('bind_url', 'ntnuita.no') }}',
)

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',
        'LOCATION': '/tmp/memcached.socket',
        'KEY_PREFIX': pkg_resources.require('slingsby')[0].version
    }
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'telemark_slingsby',
        'HOST': '{{ slingsby.get('db_host', '') }}',
        'USER': 'telemark_dbadmin',
        'PASSWORD': '{{ slingsby.db_password }}',
    },
}

STATIC_URL = '/static/'

FILESERVER = "{{ slingsby['fileserver'] }}"

FILESERVER_KEY = """{{ pillar.get('FILESERVER_KEY') }}"""

MEDIA_ROOT = '/srv/ntnuita.no/media'

EXTERNAL_MEDIA_ROOT = os.path.join(MEDIA_ROOT, 'external')

GOOGLE_API_PRIVATE_KEY = "{{ pillar.GOOGLE_API_PRIVATE_KEY }}"

{% if slingsby.get('media_url') %}
MEDIA_URL = '{{ slingsby.media_url }}'
{% endif %}

# Get's a "apps not loaded yet" if this line is not present, ref the accepted answer to this one:
# https://stackoverflow.com/questions/25244631/models-arent-loaded-yet-error-while-populating-in-django1-8-and-python2-7-8
django.setup()
