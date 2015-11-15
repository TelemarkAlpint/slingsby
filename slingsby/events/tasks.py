# -*- coding: utf-8 -*-

from ..general.utils import log_errors

from googleapiclient import discovery
from oauth2client.client import SignedJwtAssertionCredentials
from django.conf import settings
from celery import shared_task
from logging import getLogger
import httplib2

_logger = getLogger(__name__)

def create_events_calendar():
    """ Create an events calendar if none already exists. This function mostly exists for
    creating calendars for dev environments, not used in prod.
    """
    service = get_calendar_service()
    calendar = {
        'summary': 'Ting som skjer i Telemarkgruppa',
        'timeZone': 'Europe/Oslo',
    }
    cal_insert_response = service.calendars().insert(body=calendar).execute()
    public_acl = {
        'role': 'reader',
        'scope': {
            'type': 'default'
        }
    }
    acl_insert_response = service.acl().insert(calendarId=cal_insert_response['id'], body=public_acl).execute()
    return acl_insert_response


def get_calendar_service():
    name = 'calendar'
    version = 'v3'
    scope = 'https://www.googleapis.com/auth/calendar'

    # Prepare credentials, and authorize HTTP object with them.
    credentials = SignedJwtAssertionCredentials(settings.GOOGLE_API_EMAIL,
        settings.GOOGLE_API_PRIVATE_KEY, scope)
    http = credentials.authorize(http=httplib2.Http())

    # Construct a service object via the discovery service.
    service = discovery.build(name, version, http=http)
    return service


@shared_task
@log_errors
def update_google_calendar_event(event_id):
    from .models import Event
    event = Event.objects.get(pk=event_id)

    # If the event doesn't already exist on google calendar, create it
    if not event.google_calendar_id:
        _logger.info('Adding missing event to google calendar: %s', event.name)
        add_google_calender_event(event.id)
        return

    # Authenticate and construct service.
    service = get_calendar_service()

    payload = get_google_calendar_payload_for_event(event)
    results = service.events().update(calendarId=settings.GOOGLE_CALENDAR_ID,
        eventId=event.google_calendar_id, body=payload).execute()
    _logger.info('Google calendar event for %s updated: %s', event.name, results)


@shared_task
@log_errors
def add_google_calender_event(event_id):
    from .models import Event
    event = Event.objects.get(pk=event_id)

    if not event:
        _logger.warning('Could not find event to add to Google Calendar: %d', event_id)
        return

    google_payload = get_google_calendar_payload_for_event(event)
    service = get_calendar_service()
    results = service.events().insert(calendarId=settings.GOOGLE_CALENDAR_ID,
        body=google_payload).execute()
    if results.get('id'):
        event.google_calendar_id = results['id']
        event.save()
        _logger.info("Google Calendar event for event '%s' created successfully", event.name)
    else:
        _logger.error("New Google Calendar event did not have id in response, was: %s", results)


@shared_task
@log_errors
def delete_google_calendar_event(google_calendar_event_id):
    service = get_calendar_service()
    result = service.events().delete(calendarId=settings.GOOGLE_CALENDAR_ID,
        eventId=google_calendar_event_id).execute()
    _logger.info('Google calendar event %s deleted: %s', google_calendar_event_id, result)


def get_google_calendar_payload_for_event(event):
    return {
        'summary': event.name,
        'location': event.location,
        'description': event.summary,
        'start': {
            'dateTime': event.startdate.isoformat(),
            'timeZone': 'Europe/Oslo',
        },
        'end': {
            'dateTime': event.enddate.isoformat(),
            'timeZone': 'Europe/Oslo',
        }
    }
