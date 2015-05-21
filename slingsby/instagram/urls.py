from .views import AllInstagramMediaView

from django.conf.urls import patterns, url

urlpatterns = [
    url(r'^$', AllInstagramMediaView.as_view(), name='all_instagram'),
]
