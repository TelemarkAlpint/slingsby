# coding: utf-8

from .views import UserProfileView
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',
    url(r'^$', login_required(UserProfileView.as_view()), name='profile'),
)
