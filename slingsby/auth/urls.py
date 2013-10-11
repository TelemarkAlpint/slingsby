from .views import LogoutView
from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
)
