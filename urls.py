# coding: utf-8

from django.conf import settings
from django.http import HttpResponseRedirect
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic.simple import direct_to_template

admin.autodiscover()
handler500 = lambda request: direct_to_template(request, '500.html', {})

urlpatterns = patterns('',
    url(r'^join$', 'users.views.join_group', name='join'),
    url(r'^', include('articles.urls')),
    url(r'^musikk/', include('musikk.urls')),
    url(r'^arkiv/', include('archive.urls')),
    url(r'^profil/', include('users.urls')),
    url(r'^forum/', 'general.to_be_implemented'),
    url(r'^quotes/', include('quotes.urls')),
    (r'^auth/', include('auth.urls')),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^upload/', include('upload.urls')),
    (r'^tasks/', include('tasks.urls')),
    (r'^program/', include('events.urls')),
    (r'^gear/', include('gear.urls')),
                       )

urlpatterns += patterns('',
    (r'^favicon.ico$', lambda r: HttpResponseRedirect(settings.STATIC_URL + 'favicon.ico')),
    (r'^robots.txt$', lambda r: HttpResponseRedirect(settings.STATIC_URL + 'robots.txt')),
                        )
