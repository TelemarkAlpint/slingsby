from django.conf.urls import patterns, url

urlpatterns = patterns('slingsby.archive.views',
    url(r'^$', 'view_archive', name='archive'),
    (r'^update$', 'update_archive'),
    url(r'^([0-9a-f]+)', 'event_details', name='event_details'),
)
