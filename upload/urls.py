from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('upload',
    (r'^upload_quote', 'upload_quote'),
    (r'^upload_category', 'upload_category'),
    url(r'^upload_post', 'upload_post', name='upload_post'),
    (r'^event_participation', 'toggle_event_participation'),
    url(r'^submit_full_name', 'submit_full_name', name='submit_full_name'),
    )