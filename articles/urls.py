from articles.models import ArticleListView, ArticleDetailView, SubPageArticle
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    url(r'^$', ArticleListView.as_view(), name='main'),
    url(r'^artikkel/(?P<pk>\d+)', ArticleDetailView.as_view()),
    url(r'^articles/(?P<pk>\d+)', ArticleDetailView.as_view(), name='artikkel_detail'),
                        )

urls = []
for slug, article_id in SubPageArticle.objects.all().values_list('slug', 'article'):
    urls.append(url(r'^%s/$' % slug, ArticleDetailView.as_view(), {'pk': article_id}))
urlpatterns += patterns('', *urls)