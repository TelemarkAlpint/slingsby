import logging, os, sys, warnings

# Enable warnings from Django, and log them
warnings.simplefilter('default')

# Enable this to fail on DeprecationWarnings, allowing you to see which line is causing
# the warning:
#warnings.simplefilter('error', DeprecationWarning)
logging.captureWarnings(True)

# Must set this env var before importing any part of Django
os.environ['DJANGO_SETTINGS_MODULE'] = 'slingsby.settings'

from django.core.handlers.wsgi import WSGIHandler

application = WSGIHandler()
