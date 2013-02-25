# coding: utf-8

from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('users.views',
    url(r'^$', 'edit_profile', name='profile'),
                       )

