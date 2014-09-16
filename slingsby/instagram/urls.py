from .views import AllInstagramMediaView

from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', AllInstagramMediaView.as_view(), name='all_instagram'),
)
