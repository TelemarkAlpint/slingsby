from . import settings

from django.core.handlers.wsgi import WSGIHandler
from django.core.management import execute_manager
# pylint: disable=invalid-name

application = WSGIHandler()

def manage():
    execute_manager(settings)
