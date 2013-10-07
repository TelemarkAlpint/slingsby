# pylint: disable=invalid-name

from .users.views import UserProfileView
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic.base import TemplateView, RedirectView

from .archive  import urls as archive_urls
from .articles import urls as article_urls
from .auth     import urls as auth_urls
from .events   import urls as event_urls
from .gear     import urls as gear_urls
from .musikk   import urls as musikk_urls
from .quotes   import urls as quote_urls
from .tasks    import urls as task_urls
from .users    import urls as user_urls

admin.autodiscover()

handler500 = TemplateView.as_view(template_name='500.html')

urlpatterns = patterns('',
    url(r'^join$',   UserProfileView.as_view(action='join'), name='join'),
    url(r'^',        include(article_urls)),
    url(r'^musikk/', include(musikk_urls)),
    url(r'^arkiv/',  include(archive_urls)),
    url(r'^profil/', include(user_urls)),
    url(r'^quotes/', include(quote_urls)),
    (r'^auth/',      include(auth_urls)),
    (r'^tasks/',     include(task_urls)),
    (r'^program/',   include(event_urls)),
    (r'^gear/',      include(gear_urls)),
    (r'^admin/',     include(admin.site.urls)),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
)

# social auth urls
urlpatterns += patterns('',
    url(r'', include('social_auth.urls')),
)

urlpatterns += patterns('',
    (r'^favicon.ico$', RedirectView.as_view(url=settings.STATIC_URL + 'favicon.ico')),
    (r'^robots.txt$', RedirectView.as_view(url=settings.STATIC_URL + 'robots.txt')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'%s(?P<path>.*)$' % settings.STATIC_URL, 'django.views.static.serve', {'document_root': settings.STATIC_ROOT, 'show_indexes': True}),
    )
