from articles.models import ArticleDetailView, SubPageArticle
from django.conf.urls.defaults import patterns, url
from django.core.urlresolvers import reverse
from django.http import HttpResponsePermanentRedirect

urlpatterns = patterns('articles.views',
    url(r'^$', 'latest_articles', name='frontpage'),
    url(r'^artikkel/(\d+)/$', lambda req, pk: HttpResponsePermanentRedirect(reverse('article_detail', args=[str(pk)]))), #Deprecated!
    url(r'^articles/(\d+)/$', 'show_article', name='article_detail'),
    url(r'^articles/$', 'all_articles'),
                        )

urls = []
for slug, article_id in SubPageArticle.objects.all().values_list('slug', 'article'):
    urls.append(url(r'^%s/$' % slug, ArticleDetailView.as_view(), {'pk': article_id}))
urlpatterns += patterns('', *urls)