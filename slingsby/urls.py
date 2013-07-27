# coding: utf-8

from django.conf import settings
from django.http import HttpResponseRedirect
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic.simple import direct_to_template

from .archive  import urls as archive_urls
from .articles import urls as article_urls
from .auth     import urls as auth_urls
from .events   import urls as event_urls
from .gear     import urls as gear_urls
from .musikk   import urls as musikk_urls
from .quotes   import urls as quote_urls
from .tasks    import urls as task_urls
from .upload   import urls as upload_urls
from .users    import urls as user_urls

admin.autodiscover()
handler500 = lambda request: direct_to_template(request, '500.html', {})

urlpatterns = patterns('',
    url(r'^join$',   'slingsby.users.views.join_group', name='join'),
    url(r'^',        include(article_urls)),
    url(r'^musikk/', include(musikk_urls)),
    url(r'^arkiv/',  include(archive_urls)),
    url(r'^profil/', include(user_urls)),
    url(r'^quotes/', include(quote_urls)),
    (r'^auth/',      include(auth_urls)),
    (r'^upload/',    include(upload_urls)),
    (r'^tasks/',     include(task_urls)),
    (r'^program/',   include(event_urls)),
    (r'^gear/',      include(gear_urls)),
    (r'^admin/',     include(admin.site.urls)),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
                       )

urlpatterns += patterns('',
    (r'^favicon.ico$', lambda r: HttpResponseRedirect(settings.STATIC_URL + 'favicon.ico')),
    (r'^robots.txt$', lambda r: HttpResponseRedirect(settings.STATIC_URL + 'robots.txt')),
                        )
