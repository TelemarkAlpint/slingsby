from ..articles.views import SingleArticlePageQuery
from ..events.views import NextEventsQuery
from .models import SponsorsQuery

from django.conf import settings


def default(request):
    context = {
        'sponsors': SponsorsQuery.get_cached(),
        'next_events': NextEventsQuery.get_cached(),
        'subpages': SingleArticlePageQuery.get_cached(),

        # This will override what is set by django.core.context_processors.debug
        'debug': settings.DEBUG,
    }

    # only provide it present to avoid overriding template contexts
    if request.GET.get('msg'):
        context['feedback'] = request.GET.get('msg')
    return context
