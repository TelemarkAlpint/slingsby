from .views import ArchiveView, ArchiveEventDetailView
from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', ArchiveView.as_view(), name='archive'),
    url(r'^(?P<event_id>[0-9a-f]+)', ArchiveEventDetailView.as_view(), name='event_details'),
)
