# coding: utf-8

from .views import UserProfileView
from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', UserProfileView.as_view(), name='profile'),
)
