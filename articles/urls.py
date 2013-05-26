from articles.views import SingleArticlePageQuery
from django.conf.urls import patterns, url
from django.core.urlresolvers import reverse
from django.http import HttpResponsePermanentRedirect

urlpatterns = patterns('articles.views',
    url(r'^$', 'latest_articles', name='frontpage'),
    url(r'^artikkel/(\d+)/$', lambda req, pk: HttpResponsePermanentRedirect(reverse('article_detail', args=[str(pk)]))), #Deprecated!
    url(r'^articles/(\d+)/$', 'show_article', name='article_detail'),
    url(r'^articles/$', 'all_articles', name='all_articles'),
                        )

urls = []
for subpage in SingleArticlePageQuery.get_cached():
    urls.append(url(r'^%s/$' % subpage['slug'], 'articles.views.show_article', {'article_id': subpage['id']}))
urlpatterns += patterns('', *urls)