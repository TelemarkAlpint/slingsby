# pylint: disable=unused-wildcard-import,wildcard-import,invalid-name

# Override settings locally
from slingsby.settings import *
from slingsby.general.utils import MockSSHClient
from os import path
import os
import textwrap
import yaml

import sys
if len(sys.argv) >= 2 and sys.argv[1] == 'test':
    # Reduce logger verbosity in test to see only the relevant data
    import logging
    logging.disable(logging.WARNING)
    NOSE_ARGS = ['-x']

DEBUG = True

DEBUG_TOOLBAR = os.environ.get('DJANGO_DEBUG_TOOLBAR', False)

TEMPLATE_DEBUG = DEBUG

CELERY_ALWAYS_EAGER = True

SECRET_KEY = 'pleasedontusethisinprod'

SOCIAL_AUTH_FACEBOOK_SECRET = 'pleasedontusethisinprod'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db-dev.sqlite',
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        'LOCATION': 'slingsby_rel'
    }
}

AUTHENTICATION_BACKENDS = list(AUTHENTICATION_BACKENDS) + [
    'slingsby.users.DevAuthBackend',
]

# Used for the query debugger that's run in dev mode.
INTERNAL_IPS = ("127.0.0.1", "::1")

STATIC_URL = '/static/'

# This is where collectstatic gathers the static files from the installed apps
STATIC_ROOT = path.join(path.dirname(__file__), '.tmp', 'static')

# This is where static files are served from
STATICFILES_DIRS = (
   path.join(path.dirname(__file__), 'build', 'static'),
)

INSTALLED_APPS = list(INSTALLED_APPS) + [
    'django_nose',
]

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

ALLOWED_HOSTS = (
    'localhost',
    'ntnuita.local',
)

if DEBUG_TOOLBAR:
    DEBUG_TOOLBAR_CONFIG = {
        'SHOW_TOOLBAR_CALLBACK': '%s.true' % __name__,
        'SHOW_COLLAPSED': True,
    }

    def true(_):
        return True

    MIDDLEWARE_CLASSES = [
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ] + list(MIDDLEWARE_CLASSES)

    INSTALLED_APPS.append('debug_toolbar')

if os.environ.get('FILESERVER'):
    FILESERVER = os.environ.get('FILESERVER')

# This is the private key used to SSH into the travis box, pubkey added
# to .ssh/authorized_keys by .travis.yml. Only used when RUN_SSH_TESTS=1.
FILESERVER_KEY = textwrap.dedent('''\
    -----BEGIN RSA PRIVATE KEY-----
    MIIEpAIBAAKCAQEAoyOL+iiEDqQE78dTGr5QVTS3ZdVGgJbKYqSJwq4sAENwPXf1
    x9BlsgVzaKOi5i+uYlOjsHNcS8VrlB3YIcSdXeV2gThzoSdma5+vvOVyEl8Ks6Ni
    o9TMUqcuwwduL+vyUH0x/+F0Hy8L9bm2WcFUfcnM/CTkQRXODwiz/aypgpGoE/T2
    ZPZy9BV87NOu2NM2V4nbAczXmNWRzoQ3AJVbfXq+yk4231+3686v0xq/O0wfJq6s
    9xrOgVWpYa4PT3fmsVhzAwgjcgD+DhLLzwSieo82F8Uskb0n4/qBfv77d0CyF3bi
    rm8LA/4IyMFMEUJO66C+umiyRgDD2iT1QGW7eQIDAQABAoIBAQCR8MbUL1KT1l8k
    MehCUGaFEvfN/ZFoj3zV6ePjaPSr96h9FMemzONs8jtgLKMZ0SXriG8y9sBmeGHY
    yyoCa2VsDk6JIvst+5VASkZoccoubR+hvFQNw9xVRIIsroUAEc9f+d+0zPeYvfmx
    BUX/3Ve8f78FAeu/3cXM5Tg/gyrRRhZxXB+XHcHuHsWOH/9YavBIRFZ8Urb3O0g6
    YVy9UrQ4msq2zNyVrgdZBx5zaduEZK33F92fOgK8DwyUHpkb7kYtZET17PxUbpIA
    mAOrkF5r52hUy89XZmstkcO2CQy+Gx3U9oGp8Znhe1JizvFaHL0ZAKeByYDFiYf1
    yzfpurGRAoGBANReqbXO9htdgvV4hNBiRvQVCcf0AcQRA+fnJ68QzHb9wZ6oA/1r
    YFeOC/2lorgPVsz+Q6C4DL6n6Wbru3PbrMfdx5IT7TzH/Bf5lFIkBsYo3SVpbzq9
    T14cKnnbT0FDBquPRJ1XkBSRAH+ZaHIX+CrRi08H5xLxVroeq0ZZUrTbAoGBAMSn
    pEpD9Rbk+XVAMza8Fnb1VSF+1A6UQzIG5fC4pZZBBjlCuewsFBG4gN5j/x17xv2b
    Dq8n+98Fy92z4suK9MSLvB1FB5LfjrH/+ub9ZXXqGK1ePFs0uqCqXFi3u/EEJKow
    SclCLUgAkKK2BaR4fFwAzX3MmKGoa96p+lkj4Tc7AoGAeyZ524gshynu61H8Eqsq
    4hfhGCaTb5M+ZJhTFt3y832rbcmYprhBogQpR+lpNrsOZsl7hhO0sErGunwws7rL
    swsU08ziYcDGm1CLhiaGFxtTQoKlkbZ98+D5cLiQeRPZJltqOqOwVXzQgS4At0jX
    DF1/H1FB2mZBGKT4RU8++skCgYEAiO9/LCOED4wj1Kx+vPdd4TnWLLvG59v/ql85
    UFUTILxonAjFtBnBY9GJEtKou5wMJV4KbJc4AMVlfxyaqUc6R35R4EPIEVLQZ0wr
    Jxt9wgzfYCGFf7EI34WhRjmyihJrgYKcbqNBKqkSDesXpL4tQldgv99uzOqdKnBM
    HjQoyC8CgYA9SvLiRwzWfeAE9/qMwU8mrvrLr+CN1yNGHWv3b+8o2VqsjWGNMupn
    xhm0wyTPOrjpOwdKYPsAWd4tFwaFmA3A8HXurjcXqZ17Dii6/2rAoJoGosFzgqFH
    NSddVYNEowsH3azzX3txUGhHu/uxwykUGE0HKTkSjJaZHFjqtTu0eA==
    -----END RSA PRIVATE KEY-----
    ''')

MEDIA_ROOT = path.abspath('media')

SSH_CLIENT = MockSSHClient()

# When testing locally this will just be any local folder. In vagrant or prod, this will
# be a sshfs mount
EXTERNAL_MEDIA_ROOT = path.join(MEDIA_ROOT, 'external')

# Load secrets from pillar/secure/init.sls if available
secrets_file = os.path.join(os.path.dirname(__file__), 'pillar', 'secure', 'init.sls')

if path.exists(secrets_file):
    local_variables = locals()
    with open(secrets_file) as secrets_fh:
        secret_data = yaml.load(secrets_fh)
    for key, val in secret_data.items():
        local_variables[key] = val
else:
    print('Decrypted secrets not found, some functionality will not be available, notably ' +
        'social authentication.\n\nTo decrypt these secrets, run ' +
        '`python tools/secure_data.py decrypt` to do so.\nThe decryption key can be found in ' +
        'Kontoer.kdbx in the styre-dropbox')

MEDIA_URL = '/media/external/'
