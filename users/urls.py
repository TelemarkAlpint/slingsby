# coding: utf-8

from django.conf.urls import patterns, url

urlpatterns = patterns('users.views',
    url(r'^$', 'edit_profile', name='profile'),
                       )

