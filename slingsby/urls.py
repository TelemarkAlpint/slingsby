# pylint: disable=invalid-name

from .general.templatetags.revved_static import get_revved_url

from django import http
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.shortcuts import render_to_response
from django.utils.cache import add_never_cache_headers

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

def redirect_to_static(request, static_file=None):
    """ Use this to redirect static stuff with custom urls, such as /favicon.ico and /robots.txt.

    The response will be a 302 redirect (not permanent since the URL will change if target is
    modified), and with no-cache headers.
    """
    revved_url = settings.STATIC_URL + get_revved_url(static_file)
    response = http.HttpResponseRedirect(revved_url)
    add_never_cache_headers(response)
    return response


urlpatterns += patterns('',
    url(r'^favicon.ico$', redirect_to_static, {'static_file': 'favicon.ico'}),
    url(r'^robots.txt$', redirect_to_static, {'static_file': 'robots.txt'}),
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
