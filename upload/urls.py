from django.conf.urls import patterns, url

urlpatterns = patterns('upload',
    url(r'^submit_full_name', 'submit_full_name', name='submit_full_name'),
    )