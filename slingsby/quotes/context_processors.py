from ..general.cache import CachedQuery
from .models import Quote, QuoteForm
from .views import AllQuotesQuery
from random import choice as random_choice

class SuggestedQuotesQuery(CachedQuery):
    queryset = Quote.objects.filter(accepted=False).values('topic', 'quote', 'author', 'id')

def get_random_quote_or_default():
    all_quotes = AllQuotesQuery.get_cached()
    if all_quotes:
        quote = random_choice(all_quotes)
    else:
        quote = Quote()
        quote.quote = 'Ingen quotes er lastet opp enda.'
        quote.author = 'Trist teknisk ansvarlig'
    return quote

def default(request):
    context = {
        'random_quote': get_random_quote_or_default(),
        'quote_form': QuoteForm(),
               }
    if request.user.is_staff:
        context['suggested_quotes'] = SuggestedQuotesQuery.get_cached()
    return context
