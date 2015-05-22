# -*- coding: utf-8 -*-

from ..general import make_title
from ..general.views import ActionView
from .models import Quote, QuoteForm

from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView
import logging

_logger = logging.getLogger(__name__)
_all_quotes = Quote.objects.filter(accepted=True)

class QuoteDetailView(ActionView, TemplateView):

    template_name = 'quotes/show_quote.html'
    actions = ('approve',)

    def get_context_data(self, **kwargs):
        context = super(QuoteDetailView, self).get_context_data(**kwargs)
        quote_id = kwargs['quote_id']
        quote = self._find_quote(int(quote_id))
        context['quote'] = quote
        return context


    def get(self, request, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


    @method_decorator(permission_required('musikk.approve_song'))
    def approve(self, request, **kwargs):
        quote_id = kwargs['quote_id']
        quote = get_object_or_404(Quote, id=quote_id)
        quote.accepted = True
        quote.save()
        _logger.info('%s confirmed quote: %s', request.user, quote)
        messages.success(request, 'Sitatet ble godkjent!')
        return HttpResponseRedirect(quote.get_absolute_url())


    def delete(self, request, **kwargs):
        if not request.user.has_perm('quotes.delete_quote'):
            _logger.info("%s was rejected from deleting quote %d", request.user, kwargs['quote_id'])
            return HttpResponseForbidden('Du har ikke tilgang til å slette denne quoten.')
        quote_id = kwargs['quote_id']
        quote = get_object_or_404(Quote, id=quote_id)
        quote.delete()
        logging.info('%s deleted quote: %s', request.user.username, quote)
        messages.success(request, 'Quote slettet!')
        return HttpResponse('Quote slettet.', content_type='text/plain')


    def _find_quote(self, quote_id):
        """ Since all quotes most likely are cached, use that
        to find fetch the quote instead of hitting the db.
        """
        found_quote = None
        cached_quotes = _all_quotes.all()
        for quote in cached_quotes:
            if quote.id == quote_id:
                found_quote = quote
                break
        else:
            found_quote = get_object_or_404(Quote, pk=quote_id)
        return found_quote


class AllQuotesView(TemplateView):

    template_name = 'quotes/all_quotes.html'

    def get_context_data(self, **kwargs):
        context = super(AllQuotesView, self).get_context_data(**kwargs)
        quotes = _all_quotes.all()
        context = {
            'all_quotes': quotes,
            'title': make_title('Sitater'),
        }
        return context


    def get(self, request, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


    def post(self, request, **kwargs):
        context = self.get_context_data(**kwargs)
        form = QuoteForm(request.POST)
        if form.is_valid():
            quote = form.save(commit=False)
            quote.suggested_by = request.user
            quote.save()
            messages.success(request, 'Takk for forslaget, noen fra styret vil se på det ASAP!')
            return HttpResponseRedirect('/')
        else:
            context['quote_form'] = form
            messages.error(request, 'Beklager, du har visst noen feil i skjemaet, prøv på nytt er du snill!')
            return HttpResponseRedirect('/')
