from .views import AllBlogsList, LatestBlogsList, BlogDetail, BlogEditor
from django.conf.urls import patterns, url
from django.core.urlresolvers import reverse
from django.http import HttpResponsePermanentRedirect

urlpatterns = patterns('slingsby.blogs.views',
    url(r'^$', LatestBlogsList.as_view(), name='blogs'),
    url(r'^blogs/(?P<blog_id>\d+)/$',
        lambda req, **kwargs: HttpResponsePermanentRedirect(reverse('blog_detail', kwargs=kwargs))), #Deprecated!
    url(r'^blogs/(?P<blog_id>\d+)/$', BlogDetail.as_view(), name='blog_detail'),
    url(r'^blogs/$', AllBlogsList.as_view(), name='all_blogs'),
    url(r'^blog_editor/$', BlogEditor.as_view(), name='blog_editor'),
)
