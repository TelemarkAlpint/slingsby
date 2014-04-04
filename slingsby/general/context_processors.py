from ..articles.views import SingleArticlePageQuery
from ..events.models import Event
from ..general import time
from .models import SponsorsQuery

from django.conf import settings
from django.core.urlresolvers import reverse


def default(request):
    context = {
        'sponsors': SponsorsQuery.get_cached(),
        'next_events': Event.objects.filter(enddate__gte=time.now()).values('id', 'name', 'startdate')[:3],
        'subpages': SingleArticlePageQuery.get_cached(),

        # This will override what is set by django.core.context_processors.debug
        'debug': settings.DEBUG,
    }
    return context


def slingsby_urls(request):
    """ Add url base paths that can be used in javascript.

    Using these values can reduce hard-coding URLs also for client-side scripts
    that can't use the django url template tag.
    """
    urls = {
        'STATIC_URL': settings.STATIC_URL,
        'GRAPHICS_URL': settings.STATIC_URL + 'gfx/',
        'allArticles': reverse('all_articles'),
    }
    return {
        'slingsby_urls': urls,
    }


def slingsby_config(request):
    """ Add a dictionary of config values that can be used to look up configuration
    values client-side.
    """
    config = {
        'DISQUS_IDENTIFIER': settings.DISQUS_IDENTIFIER,
    }
    return {
        'slingsby_config': config,
    }
