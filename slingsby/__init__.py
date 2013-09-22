from django.core.handlers.wsgi import WSGIHandler
import os
# pylint: disable=invalid-name

os.environ['DJANGO_SETTINGS_MODULE'] = 'slingsby.settings'

application = WSGIHandler()
