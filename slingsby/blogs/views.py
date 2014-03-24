from ..general import make_title
from ..general.cache import CachedQuery, empty_on_changes_to
from ..general.time import aware_from_utc
from ..general.mixins import JSONMixin
from .models import Blog
from dateutil.parser import parse
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView
from logging import getLogger

_logger = getLogger(__name__)

@empty_on_changes_to(Blog)
class LatestBlogsQuery(CachedQuery):
    queryset = Blog.objects.all().select_related()[:5]


@empty_on_changes_to(Blog)
class AllBlogsQuery(CachedQuery):
    queryset = Blog.objects.all().select_related()


class AllBlogsList(JSONMixin, TemplateView):

    template_name = 'blogs/blog_list.html'

    def get_context_data(self, **kwargs):
        """ Get all blogs, but filter them by the `before` param and limit
        the number of results to the `limit` param.
        """
        context = super(AllBlogsList, self).get_context_data(**kwargs)
        before = self.request.GET.get('before')
        if before is None:
            blogs = AllBlogsQuery.get_cached()
        else:
            published_date_filter = parse(before)
            utc_date = aware_from_utc(published_date_filter)
            blogs = Blog.objects.filter(published_date__lt=utc_date, visible=True)
        num_limit = int(self.request.GET.get('limit', '0'))
        if num_limit:
            blogs = blogs[:num_limit]
        context['blogs'] = blogs
        return context

    def get_json(self, request, **kwargs):
        context = self.get_context_data(**kwargs)
        return {'blogs': [blog.__json__() for blog in context['blogs']]}


class LatestBlogsList(TemplateView):

    template_name = 'blogs/blog_list.html'

    def get_context_data(self, **kwargs):
        context = super(LatestBlogsList, self).get_context_data(**kwargs)
        context['blogs'] = LatestBlogsQuery.get_cached()
        return context


class BlogDetail(TemplateView):

    template_name = 'blogs/blog_detail.html'

    def get_context_data(self, **kwargs):
        context = super(BlogDetail, self).get_context_data(**kwargs)
        blog_id = kwargs['blog_id']
        blog = get_object_or_404(Blog, pk=blog_id)
        context['blog'] = blog
        context['title'] =  make_title(blog.title)
        return context

class BlogEditor(TemplateView):

    template_name = 'blogs/blog_editor.html'