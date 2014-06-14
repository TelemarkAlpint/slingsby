from __future__ import absolute_import

from celery import Celery
from django.conf import settings
import os

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'slingsby.settings')

app = Celery('slingsby') # pylint: disable=invalid-name

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
