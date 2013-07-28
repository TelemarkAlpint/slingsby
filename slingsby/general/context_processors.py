from ..articles.views import SingleArticlePageQuery
from ..events.views import NextEventsQuery
from .constants import LOGIN_URL, MEDIA_DIR, JOIN_URL, LEAVE_URL
from .models import SponsorsQuery
from django.conf import settings

import logging

def default(request):
    logging.info("Request from context processor: %s", request)
    context = {
        'sponsors': SponsorsQuery.get_cached(),
        'next_events': NextEventsQuery.get_cached(),
        'MEDIA_DIR': MEDIA_DIR,
        'LOGIN_URL': LOGIN_URL,
        'JOIN_URL': JOIN_URL,
        'LEAVE_URL': LEAVE_URL,
        'subpages': SingleArticlePageQuery.get_cached(),


        #This will override what is set by django.core.context_processors.debug
        'debug': settings.DEBUG,
    }

    # only provide it present to avoid overriding template contexts
    if request.GET.get('msg'):
        context['feedback'] = request.GET.get('msg')
    return context
