from quotes.models import Quote, QuoteForm
from quotes.views import AllQuotesQuery
from random import choice as random_choice

def get_random_quote_or_default():
    all_quotes = AllQuotesQuery.get_cached()
    if all_quotes:
        quote = random_choice(all_quotes)
    else:
        quote = Quote()
        quote.quote = 'Ingen quotes er lastet opp enda.'
        quote.author = 'Trist teknisk ansvarlig'
    return quote

def get_new_quote_suggestions():
    suggested_quotes = Quote.objects.filter(accepted=False)
    return suggested_quotes

def default(request):
    context = {
        'random_quote': get_random_quote_or_default(),
        'quote_form': QuoteForm(),
        'suggested_quotes': get_new_quote_suggestions(),
               }
    return context