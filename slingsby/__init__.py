from django.core.handlers.wsgi import WSGIHandler
import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'slingsby.settings'

application = WSGIHandler()
