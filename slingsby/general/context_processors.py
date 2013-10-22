from ..articles.views import SingleArticlePageQuery
from ..events.views import NextEventsQuery
from .models import SponsorsQuery

from django.conf import settings
from django.core.urlresolvers import reverse


def default(request):
    context = {
        'sponsors': SponsorsQuery.get_cached(),
        'next_events': NextEventsQuery.get_cached(),
        'subpages': SingleArticlePageQuery.get_cached(),

        # This will override what is set by django.core.context_processors.debug
        'debug': settings.DEBUG,
    }
    return context

def urls(request):
    urls = {
        'STATIC_URL': settings.STATIC_URL,
        'GRAPHICS_URL': settings.STATIC_URL + 'gfx/',
        'allArticles': reverse('all_articles'),
    }
    return {
        'slingsby_urls': urls,
    }
