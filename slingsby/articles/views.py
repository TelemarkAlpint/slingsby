from ..general import make_title
from ..general.cache import CachedQuery
from ..general.time import aware_from_utc
from .models import SubPageArticle, Article
from dateutil.parser import parse
from django.db.models.signals import post_save, post_delete
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView
import json
import logging

logger = logging.getLogger(__name__)

class SingleArticlePageQuery(CachedQuery):
    queryset = SubPageArticle.objects.all()
post_save.connect(SingleArticlePageQuery.empty_on_save, sender=SubPageArticle)
post_delete.connect(SingleArticlePageQuery.empty_on_save, sender=SubPageArticle)


class LatestArticlesQuery(CachedQuery):
    queryset = Article.objects.all().select_related()[:5]
post_save.connect(LatestArticlesQuery.empty_on_save, sender=Article)


class AllArticlesQuery(CachedQuery):
    queryset = Article.objects.all().select_related()
post_save.connect(AllArticlesQuery.empty_on_save, sender=Article)


class AllArticlesList(TemplateView):

    template_name = 'articles/article_list.html'

    def _get_filtered_articles(self, request):
        """ Get all articles, but filter them by the `before` param and limit
        the number of results to the `limit` param.
        """
        before = request.GET.get('before')
        if before is None:
            articles = AllArticlesQuery.get_cached()
        else:
            published_date_filter = parse(before)
            utc_date = aware_from_utc(published_date_filter)
            articles = Article.objects.filter(published_date__lt=utc_date, visible=True)
        num_limit = int(request.GET.get('limit', '0'))
        if num_limit:
            articles = articles[:num_limit]
        return articles

    def get(self, request):
        articles = self._get_filtered_articles(request)
        if request.prefer_json:
            json_data = {
                'articles': [a.__json__() for a in articles],
            }
            return HttpResponse(json.dumps(json_data), mimetype='application/json')
        context = {
            'articles': articles,
        }
        return self.render_to_response(context)


class LatestArticlesList(TemplateView):

    template_name = 'articles/article_list.html'

    def get_context_data(self, **kwargs):
        context = {
            'articles': LatestArticlesQuery.get_cached(),
        }
        return context


class ArticleDetail(TemplateView):

    template_name = 'articles/article_detail.html'

    def get(self, request, article_id):
        try:
            article = get_object_or_404(Article, pk=article_id)
        except Http404:
            article = get_object_or_404(SubPageArticle, pk=article_id)
        if request.prefer_json:
            return HttpResponse(json.dumps(article.__json__()), mimetype='application/json')
        context = {
            'article': article,
            'title': make_title(article.title),
        }
        return self.render_to_response(context)
