{% set slingsby = pillar.get('slingsby', {}) -%}

from slingsby.settings import *

import django

SECRET_KEY = '{{ slingsby.secret_key }}'

SOCIAL_AUTH_FACEBOOK_SECRET = '{{ pillar.get("SOCIAL_AUTH_FACEBOOK_SECRET", 'youneedmorefootodothis') }}'

ALLOWED_HOSTS = (
    '{{ slingsby.get('bind_url', 'ntnuita.no') }}',

    # localhost needed so that curl can access /tasks/
    'localhost',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'slingsby_rel',
        'HOST': '{{ pillar['env']['db_uri'] }}',
        'USER': 'slingsby',
        'PASSWORD': '{{ slingsby.db_password }}',
    },
}

STATIC_URL = '/static/'

FILESERVER = "{{ slingsby.get('fileserver', 'tarjeikl@login.stud.ntnu.no') }}"

FILESERVER_MEDIA_ROOT = "{{ slingsby.get('fileserver_media_root', '/home/groupswww/telemark/media/') }}"

FILESERVER_KEY = """{{ pillar.get('FILESERVER_KEY') }}"""

MEDIA_ROOT = '/srv/ntnuita.no/media'

{% if slingsby.get('media_url') %}
MEDIA_URL = '{{ slingsby.media_url }}'
{% endif %}

# Get's a "apps not loaded yet" if this line is not present, ref the accepted answer to this one:
# https://stackoverflow.com/questions/25244631/models-arent-loaded-yet-error-while-populating-in-django1-8-and-python2-7-8
django.setup()
