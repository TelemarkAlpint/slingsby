from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic.simple import direct_to_template
from events.models import Event
from general import make_title
import json

def detail(request, event_id):
    event_id = int(event_id)
    event = get_object_or_404(Event, pk=event_id)
    if request.prefer_json:
        return HttpResponse(json.dumps(event.__json__()), mimetype='application/json')
    values = {
              'event': event,
              'title': make_title(event.name),
              }
    return direct_to_template(request, 'events/event_detail.html', values)