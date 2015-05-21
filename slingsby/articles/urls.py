from .views import SingleArticlePageQuery, AllArticlesList, Frontpage, ArticleDetail
from django.conf.urls import patterns, url
from django.core.urlresolvers import reverse
from django.http import HttpResponsePermanentRedirect

urlpatterns = [
    url(r'^$', Frontpage.as_view(), name='frontpage'),
    url(r'^articles$', AllArticlesList.as_view(), name='all_articles'),
    url(r'^articles/(?P<article_id>\d+)$', ArticleDetail.as_view(), name='article_detail'),

    # Redirect from old /artikkel-URLs to /articles
    url(r'^artikkel/(?P<article_id>\d+)$',
        lambda req, **kwargs: HttpResponsePermanentRedirect(reverse('article_detail', kwargs=kwargs))),
]

# TODO: Fetching subpages is half of the database query time on normal pages, needs to be optimized
for subpage in SingleArticlePageQuery.get_cached():
    urlpatterns += [url(r'^%s$' % subpage.slug, ArticleDetail.as_view(), {'article_id': subpage.id})]
