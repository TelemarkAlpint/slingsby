# coding: utf-8

from .models import Event, UserAddError, EventError
from ..general import make_title, add_params, feedback, time
from ..general.cache import CachedQuery
from django.db.models.signals import post_save
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.safestring import SafeUnicode
from django.views.decorators.http import require_POST
from django.views.generic.simple import direct_to_template
import json
from logging import getLogger

logger = getLogger(__name__)

class AllUpcomingEventsQuery(CachedQuery):
    queryset = Event.objects.filter(startdate__gte=time.now())
post_save.connect(AllUpcomingEventsQuery.empty_on_save, sender=Event)

class NextEventsQuery(CachedQuery):
    queryset = Event.objects.filter(startdate__gte=time.now()).values('id', 'name', 'startdate')[:3]
    timeout_in_s = 3600
post_save.connect(NextEventsQuery.empty_on_save, sender=Event)

def list_events(request):
    events = AllUpcomingEventsQuery.get_cached()
    if request.prefer_json:
        json_data = {
                     'events': [event.__json__() for event in events],
                     }
        return HttpResponse(json.dumps(json_data), mimetype='application/json')
    context = {
               'events': events,
               'title': make_title('Program'),
               }
    return direct_to_template(request, 'events/event_list.html', context)

def detail(request, event_id):
    event_id = int(event_id)
    event = get_object_or_404(Event, pk=event_id)
    if request.prefer_json:
        json_data = {
                     'event': event.__json__(),
                    }
        return HttpResponse(json.dumps(json_data), mimetype='application/json')
    values = {
              'event': event,
              'title': make_title(event.name),
              }
    return direct_to_template(request, 'events/event_detail.html', values)

@require_POST
def join_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    redirect = event.get_absolute_url()
    user = request.user
    try:
        event.add_user(user)
    except UserAddError as error:
        logger.info(error)
        logger.info('%s meldte seg på eventet %s.', user, event)
    redirect = add_params(redirect, feedback.EVENT_SIGN_ON.format_string(event))
    return HttpResponseRedirect(redirect)

@require_POST
def leave_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    user = request.user
    try:
        event.remove_user(user)
        redirect = add_params(event.get_absolute_url(),
                              feedback.EVENT_SIGN_OFF.format_string(event))
        logger.info('%s meldte seg av eventet %s.', user, event)
        logger.info('Redirect: ' + redirect)
        return HttpResponseRedirect(redirect)
    except EventError as error:
        logger.warning(error)
        logger.warning('%s tried to unregister from the binding event "%s"' % (user.username, event.name))
        return direct_to_template(request, 'infopage.html',
                                    {'content': SafeUnicode('''Beklager, men dette eventet har bindende påmelding. Ta
                                    kontakt med arrkom hvis du absolutt ikke har mulighet til å stille,
                                    så vil vi se om vi kan gjøre noe med det.''')})
