from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models.signals import post_save
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.views.generic.simple import direct_to_template
from general import make_title, reverse_with_params, feedback
from general.cache import CachedQuery
from quotes.models import Quote, QuoteForm
import json
import logging
from upload import upload

logger = logging.getLogger(__name__)

class AllQuotesQuery(CachedQuery):
    queryset = Quote.objects.filter(accepted=True).values('topic', 'quote', 'author')

post_save.connect(AllQuotesQuery.empty_on_save, sender=Quote)

@staff_member_required
@require_POST
def approve_quote(request, quote_id):
    quote = get_object_or_404(Quote, id=quote_id)
    quote.accepted = True
    quote.save()
    logger.info('%s confirmed quote: %s', request.user.username, quote)
    return HttpResponseRedirect(quote.get_absolute_url())

@staff_member_required
@require_POST
def delete_quote(request, quote_id):
    quote = get_object_or_404(Quote, id=quote_id)
    quote.delete()
    logging.info('%s rejected quote: %s', request.user.username, quote)
    return HttpResponse('Quote slettet.', content_type='text/plain')

@login_required
@require_POST
def upload_quote(request):
    redirect = reverse_with_params(feedback_code=feedback.QUOTE_THANKS)
    return upload(request, QuoteForm, reverse('upload_quote'), redirect)

def all_quotes(request):
    quotes = AllQuotesQuery.update_cache()
    if request.prefer_json:
        if 'pending' in request.GET:
            logger.info('Verbose JSON of all quotes returned')
            quotes = Quote.objects.all()
            json_array = [quote.__json__(verbose=True) for quote in quotes]
        else:
            logger.info('JSON of all quotes returned.')
            json_array = [quote.__json__() for quote in quotes]
        return HttpResponse(json.dumps(json_array), mimetype='application/json')
    context = {
               'all_quotes': quotes,
               'title': make_title('Sitater'),
               }
    return direct_to_template(request, 'quotes/all_quotes.html', context)

def find_quote(quote_id):
    found_quote = None
    cached_quotes = AllQuotesQuery.get_cached()
    for quote in cached_quotes:
        if quote.id == quote_id:
            found_quote = quote
            break
    else:
        found_quote = get_object_or_404(Quote, pk=quote_id)
    return found_quote

def show_quote(request, quote_id):
    quote = find_quote(int(quote_id))
    if request.prefer_json:
        json_dict = None
        if 'pending' in request.GET:
            json_dict = quote.__json__(verbose=True)
        else:
            json_dict = quote.__json__()
        return HttpResponse(json.dumps(json_dict), mimetype='application/json')
    return direct_to_template(request, 'quotes/show_quote.html', {'quote': quote})