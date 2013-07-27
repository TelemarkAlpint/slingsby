from .views import SingleArticlePageQuery, AllArticlesList, LatestArticlesList, ArticleDetail
from django.conf.urls import patterns, url
from django.core.urlresolvers import reverse
from django.http import HttpResponsePermanentRedirect

urlpatterns = patterns('slingsby.articles.views',
    url(r'^$', LatestArticlesList.as_view(), name='frontpage'),
    url(r'^artikkel/(\d+)/$', lambda req, pk: HttpResponsePermanentRedirect(reverse(ArticleDetail.as_view(), args=[str(pk)]))), #Deprecated!
    url(r'^articles/(\d+)/$', ArticleDetail.as_view(), name='article_detail'),
    url(r'^articles/$', AllArticlesList.as_view(), name='all_articles'),
                        )

urls = []
for subpage in SingleArticlePageQuery.get_cached():
    urls.append(url(r'^%s/$' % subpage.slug, ArticleDetail.as_view(), {'article_id': subpage.id}))
urlpatterns += patterns('', *urls)
