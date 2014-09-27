# pylint: disable=invalid-name

from .general.templatetags.revved_static import get_revved_url

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic.base import RedirectView
from django.shortcuts import render_to_response

admin.autodiscover()

handler500 = lambda req: render_to_response('500.html')

urlpatterns = patterns('',
    url(r'^', include('slingsby.articles.urls')),
    url(r'^musikk/', include('slingsby.musikk.urls')),
    url(r'^arkiv/', include('slingsby.archive.urls')),
    url(r'^profil/', include('slingsby.users.urls')),
    url(r'^quotes/', include('slingsby.quotes.urls')),
    url(r'^instagram/', include('slingsby.instagram.urls')),
    (r'^auth/', include('slingsby.auth.urls')),
    (r'^tasks/', include('slingsby.tasks.urls')),
    (r'^program/', include('slingsby.events.urls')),
    (r'^gear/', include('slingsby.gear.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
)

# social auth urls
urlpatterns += patterns('',
    url(r'', include('social.apps.django_app.urls', namespace='social')),
)

urlpatterns += patterns('',
    (r'^favicon.ico$', RedirectView.as_view(url=get_revved_url('favicon.ico'))),
    (r'^robots.txt$', RedirectView.as_view(url=get_revved_url('robots.txt'))),
)

if settings.DEBUG:
    from .users.views import DevLogin
    urlpatterns += patterns('',
        url(r'^devlogin/', DevLogin.as_view(), name='devlogin')
    )
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar
        urlpatterns += patterns('',
            url(r'^__debug__/', include(debug_toolbar.urls)),
        )
