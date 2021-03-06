# coding: utf-8

from .models import Event, UserAddError, EventError, _format_date
from ..general import make_title, time
from ..general.views import ActionView

from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView
from logging import getLogger

_logger = getLogger(__name__)

class EventListView(TemplateView):

    template_name = 'events/event_list.html'

    def get_context_data(self, **kwargs):
        context = super(EventListView, self).get_context_data(**kwargs)
        events = Event.objects.filter(enddate__gte=time.now())
        context['events'] = events
        context['title'] = make_title('Program')
        context['calendar_id'] = settings.GOOGLE_CALENDAR_ID
        return context

    def get(self, request, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class EventDetailView(ActionView, TemplateView):

    template_name = 'events/event_detail.html'
    actions = ('join', 'leave')

    def get_context_data(self, **kwargs):
        context = super(EventDetailView, self).get_context_data(**kwargs)
        event_id = kwargs['event_id']
        event = get_object_or_404(Event, pk=event_id)
        context['event'] = event
        context['title'] = make_title(event.name)
        context['user_is_signed_up'] = event.is_user_participant(self.request.user)
        context['event_open_for_user'] = event.can_user_register_now(self.request.user)
        context['participating_users'] = event.get_participating_users(self.request.user)
        if event.registration_opens:
            context['registration_opens_for_user_as_string'] = _format_date(time.utc_to_nor(
                event.registration_opens_for_user(self.request.user)))
            context['signup_countdown_seconds'] = event.signup_countdown_seconds(
                self.request.user)
        return context


    def get(self, request, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


    def join(self, request, **kwargs):
        _logger.info('%s prøver å melde seg på et event', request.user)
        event_id = kwargs['event_id']
        event = get_object_or_404(Event, pk=event_id)
        try:
            event.add_user(request.user)
            _logger.info("%s meldte seg på eventet %s", request.user, event)
            messages.success(request, 'Du er nå påmeldt %s!' % event)
        except UserAddError as error:
            _logger.info(error)
            messages.error(request, error.reason)
            return self.render_to_response(self.get_context_data(**kwargs), status=400)
        return HttpResponseRedirect(event.get_absolute_url())


    def leave(self, request, **kwargs):
        _logger.info('%s prøver å melde seg av et event', request.user)
        event_id = kwargs['event_id']
        event = get_object_or_404(Event, pk=event_id)
        try:
            event.remove_user(request.user)
            _logger.info('%s meldte seg av eventet %s.', request.user, event)
            messages.info(request, 'Du har nå meldt deg av %s.' % event)
            return HttpResponseRedirect(event.get_absolute_url())
        except EventError as error:
            _logger.warning(error)
            messages.warning(request, 'Beklager, men dette eventet har bindende påmelding. Ta ' \
                'kontakt med arrkom hvis du absolutt ikke har mulighet til å stille, ' \
                'så vil vi se om vi kan gjøre noe med det.')
            return HttpResponseRedirect(event.get_absolute_url())
