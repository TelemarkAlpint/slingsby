# pylint: disable=invalid-name

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic.base import RedirectView
from django.shortcuts import render_to_response

from .archive  import urls as archive_urls
from .articles import urls as article_urls
from .auth     import urls as auth_urls
from .events   import urls as event_urls
from .gear     import urls as gear_urls
from .musikk   import urls as musikk_urls
from .quotes   import urls as quote_urls
from .tasks    import urls as task_urls
from .users    import urls as user_urls
from .blogs    import urls as blog_urls

admin.autodiscover()

handler500 = lambda req: render_to_response('500.html')

urlpatterns = patterns('',
    url(r'^',        include(article_urls)),
    url(r'^musikk/', include(musikk_urls)),
    url(r'^arkiv/',  include(archive_urls)),
    url(r'^profil/', include(user_urls)),
    url(r'^quotes/', include(quote_urls)),
    (r'^auth/',      include(auth_urls)),
    (r'^tasks/',     include(task_urls)),
    (r'^program/',   include(event_urls)),
    (r'^gear/',      include(gear_urls)),
    (r'^blog/',      include(blog_urls)),
    (r'^admin/',     include(admin.site.urls)),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
)

# social auth urls
urlpatterns += patterns('',
    url(r'', include('social.apps.django_app.urls', namespace='social')),
)

urlpatterns += patterns('',
    (r'^favicon.ico$', RedirectView.as_view(url=settings.STATIC_URL + 'favicon.ico')),
    (r'^robots.txt$', RedirectView.as_view(url=settings.STATIC_URL + 'robots.txt')),
)

# Needed since we can't use the url tag for the pre-uglified scripts
# Note that this matches any url with static/ in it, so be aware of naming conflicts!
if settings.DEBUG:
    urlpatterns += patterns('django.contrib.staticfiles.views',
        url(r'static/(?P<path>.*)$', 'serve'),
    )
