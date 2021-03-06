from .views import ArchiveView, EventDetailView
from django.conf.urls import url

urlpatterns = [
    url(r'^$', ArchiveView.as_view(), name='archive'),
    url(r'^/(?P<event_id>\d+)', EventDetailView.as_view(), name='event_details'),
]
