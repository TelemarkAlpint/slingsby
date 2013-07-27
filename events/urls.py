from django.conf.urls import patterns, url

urlpatterns = patterns('events.views',
      url(r'^$', 'list_events', name='program'),
      url(r'^(\d+L?)/join/$', 'join_event', name='join_event'),
      url(r'^(\d+L?)/leave/$', 'leave_event', name='leave_event'),
      url(r'^(\d+L?)/$', 'detail', name='event_detail'),
      )
