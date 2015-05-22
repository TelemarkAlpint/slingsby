from .views import EventListView, EventDetailView
from django.conf.urls import url
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^$', EventListView.as_view(), name='program'),
    url(r'^/(?P<event_id>\d+L?)$', EventDetailView.as_view(), name='event_detail'),
    url(r'^/(?P<event_id>\d+L?)/join$', login_required(EventDetailView.as_view(action='join')), name='join_event'),
    url(r'^/(?P<event_id>\d+L?)/leave$', login_required(EventDetailView.as_view(action='leave')), name='leave_event'),
]
