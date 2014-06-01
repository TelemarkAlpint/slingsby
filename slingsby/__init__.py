from django.core.handlers.wsgi import WSGIHandler
from django.core.management import execute_from_command_line
import sys
# pylint: disable=invalid-name

application = WSGIHandler()

def manage():
    execute_from_command_line(sys.argv)
