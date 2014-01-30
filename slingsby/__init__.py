# pylint: disable=invalid-name

from django.core.handlers.wsgi import WSGIHandler
from django.core.management import execute_from_command_line

application = WSGIHandler()

def manage():
    execute_from_command_line()
