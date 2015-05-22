from .models import Quote, QuoteForm
from random import randint


def get_random_quote_or_default():
    number_of_quotes = Quote.objects.filter(accepted=True).count()
    if number_of_quotes:
        quote = Quote.objects.filter(accepted=True)[randint(0, number_of_quotes-1)]
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
    if request.user.has_perm('quotes.approve_quote'):
        context['suggested_quotes'] = Quote.objects.filter(accepted=False).values('topic', 'quote', 'author', 'id')
    return context
