from articles.views import SingleArticlePageQuery
from events.views import NextEventsQuery
from general.constants import LOGIN_URL, MEDIA_DIR, JOIN_URL, LEAVE_URL
from general.feedback import get_feedback
from general.models import SponsorsQuery
from django.conf import settings

def get_feedback_code(get_dict):
    urlcode = None
    if get_dict:
        urlcode = get_dict.keys()[0]
    return urlcode

def default(request):
    feedback_code = get_feedback_code(request.GET)
    feedback = get_feedback(feedback_code)
    context = {
        'sponsors': SponsorsQuery.get_cached(),
        'next_events': NextEventsQuery.get_cached(),
        'MEDIA_DIR': MEDIA_DIR,
        'LOGIN_URL': LOGIN_URL,
        'JOIN_URL': JOIN_URL,
        'LEAVE_URL': LEAVE_URL,
        'subpages': SingleArticlePageQuery.get_cached(),
        'feedback': feedback,
        #This will override what is set by django.core.context_processors.debug
        'debug': settings.DEBUG,
    }
    return context