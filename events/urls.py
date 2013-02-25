from django.conf.urls.defaults import patterns, url
from events.models import EventListView

urlpatterns = patterns('',
      url(r'^$', EventListView.as_view(), name='program'),
      (r'^(\d+L?)/$', 'events.views.detail'),
      )