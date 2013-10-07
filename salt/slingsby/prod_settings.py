from slingsby.settings import *

SECRET_KEY = '{{ pillar["SECRET_KEY"] }}'

FACEBOOK_API_KEY = '{{ pillar["FACEBOOK_API_KEY"] }}'

ALLOWED_HOSTS = (
    '.ntnuita.no',
)
