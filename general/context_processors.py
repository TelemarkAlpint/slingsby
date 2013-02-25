from articles.models import SubPageArticle, SingleArticlePageQuery
from events.models import NextEventsQuery
from general import make_title, cache
from general.constants import STATIC_DIR, LOGIN_URL, MEDIA_DIR, GRAPHICS_DIR, \
    JOIN_URL, LEAVE_URL
from general.feedback import get_feedback
from general.models import SponsorsQuery
from quotes.models import Quote, default_quote, QuoteForm
from quotes.views import AllQuotesQuery
from random import choice as random_choice

def get_random_quote_or_default():
    all_quotes = AllQuotesQuery.get_cached()
    if all_quotes:
        quote = random_choice(all_quotes)
    else:
        quote = default_quote()
    return quote

def get_feedback_code(get_dict):
    urlcode = None
    if get_dict:
        urlcode = get_dict.keys()[0]
    return urlcode

def get_single_article_pages():
    subpages = cache.get('subpages')
    if subpages is None:
        subpages = SubPageArticle.objects.all().values_list('slug', 'subpage_name')
        cache.set('subpages', subpages)
    return subpages

def default(request):
    feedback_code = get_feedback_code(request.GET)
    feedback = get_feedback(feedback_code)
    suggested_quotes = []
    if request.user.is_staff:
        suggested_quotes = Quote.objects.filter(accepted=False)
    return {
        'random_quote': get_random_quote_or_default(),
        'quote_form': QuoteForm(),
        'sponsors': SponsorsQuery.get_cached(),
        'next_events': NextEventsQuery.get_cached(),
        'STATIC_DIR': STATIC_DIR,
        'MEDIA_DIR': MEDIA_DIR,
        'GRAPHICS_DIR': GRAPHICS_DIR,
        'LOGIN_URL': LOGIN_URL,
        'JOIN_URL': JOIN_URL,
        'LEAVE_URL': LEAVE_URL,
        'fallback_title': make_title(),
        'subpages': SingleArticlePageQuery.get_cached(),
        'feedback': feedback,
        'suggested_quotes': suggested_quotes,
    }