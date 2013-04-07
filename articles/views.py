from articles.models import SubPageArticle, Article
from django.db.models.signals import post_save, post_delete
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic.simple import direct_to_template
from dateutil.parser import parse
from general.cache import CachedQuery
import json
import logging

logger = logging.getLogger(__name__)

class SingleArticlePageQuery(CachedQuery):
    queryset = SubPageArticle.objects.all().values_list('slug', 'subpage_name')
post_save.connect(SingleArticlePageQuery.empty_on_save, sender=SubPageArticle)
post_delete.connect(SingleArticlePageQuery.empty_on_save, sender=SubPageArticle)

class LatestArticlesQuery(CachedQuery):
    subpage_ids = list(SubPageArticle.objects.all().values_list('article', flat=True))
    queryset = Article.objects.exclude(id__in=subpage_ids) if subpage_ids else Article.objects.all()[:5]
post_save.connect(LatestArticlesQuery.empty_on_save, sender=Article)

class AllArticlesQuery(CachedQuery):
    queryset = Article.objects.all()
post_save.connect(AllArticlesQuery.empty_on_save, sender=Article)

def latest_articles(request):
    values = {
              'articles': LatestArticlesQuery.get_cached(),
              }
    return direct_to_template(request, 'articles/article_list.html', values)

def _get_filtered_articles(request):
    before = request.GET.get('before')
    if before is None:
        articles = AllArticlesQuery.get_cached()
    else:
        published_date_filter = parse(before)
        articles = Article.objects.filter(published_date__lt=published_date_filter)
    num_limit = int(request.GET.get('limit', '0'))
    if num_limit:
        articles = articles[:num_limit]
    return articles

def all_articles(request):
    articles = _get_filtered_articles(request)
    if request.prefer_json:
        json_data = {
                     'articles': [a.__json__() for a in articles],
                     }
        return HttpResponse(json.dumps(json_data), mimetype='application/json')
    values = {
              'articles': articles,
              }
    return direct_to_template(request, 'articles/article_list.html', values)

def show_article(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    if request.prefer_json:
        return HttpResponse(json.dumps(article.__json__()), mimetype='application/json')
    context = {
               'article': article,
               }
    return direct_to_template(request, 'articles/article_detail.html', context)