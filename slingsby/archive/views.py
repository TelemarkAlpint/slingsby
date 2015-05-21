# coding: utf-8
# pylint: disable=unpacking-non-sequence

from ..general import make_title
from ..general.mixins import JSONMixin
from .models import Event, Image, EventForm

from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView
from logging import getLogger

_logger = getLogger(__name__)

class ArchiveView(TemplateView):

    template_name = 'archive/archive_list.html'

    def get_context_data(self, **kwargs):
        context = super(ArchiveView, self).get_context_data(**kwargs)
        events = [e for e in Event.objects.all()]
        context['events'] = events
        context['title'] = make_title('Arkiv')
        context['event_form'] = EventForm()
        context['show_event'] = int(self.request.GET.get('showEvent', '0'))
        return context


    def post(self, request, **kwargs):
        if not request.user.has_perm('archive.can_upload_images'):
            return HttpResponseForbidden()

        form = EventForm(request.POST)
        context = self.get_context_data(**kwargs)
        uploaded_images = request.FILES.getlist('images')
        photographer = request.POST.get('photographer', '')
        if form.is_valid() and uploaded_images:
            year = form.data['startdate'].split('-')[0]
            existing_event = Event.objects.filter(startdate__contains=year, name__iexact=form.data['name'])
            event = existing_event[0] if existing_event else form.save()
            for image in uploaded_images:
                Image.objects.create(original=image, original_filename=image.name, event=event,
                    photographer=photographer)
            messages.info(request, 'Bildene ble lastet opp, vennligst vent mens vi nedskalerer dem og ' +
                'flytter dem over på filserveren, kom tilbake snart!')
            return HttpResponseRedirect(reverse('archive'))
        else:
            messages.warning(request, 'Oops, ser ut til at du har noen feil i opplastingsskjemaet, prøv ' +
                'en gang til!')
            context['event_form'] = form
            return self.render_to_response(context, status=400)


class EventDetailView(JSONMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = super(EventDetailView, self).get_context_data(**kwargs)
        event_id = kwargs['event_id']
        event = get_object_or_404(Event, pk=event_id)
        context['event'] = event
        return context


    def get_json(self, request, **kwargs):
        context = self.get_context_data(**kwargs)
        event = context['event']
        return {'event': event.to_json()}
