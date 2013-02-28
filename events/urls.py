from django.conf.urls.defaults import patterns, url
from events.models import EventListView

urlpatterns = patterns('events.views',
      url(r'^$', EventListView.as_view(), name='program'),
      url(r'^(\d+L?)/join/$', 'join_event', name='join_event'),
      url(r'^(\d+L?)/leave/$', 'leave_event', name='leave_event'),
      (r'^(\d+L?)/$', 'detail'),
      )