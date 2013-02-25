from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('upload',
    (r'^upload_quote', 'upload_quote'),
    (r'^event_participation', 'toggle_event_participation'),
    url(r'^submit_full_name', 'submit_full_name', name='submit_full_name'),
    )