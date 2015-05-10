# coding: utf-8

from __future__ import unicode_literals

from ..general import time, validate_text
from ..general.widgets import WidgEditorWidget
from datetime import timedelta
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.forms.models import ModelForm
from django.utils.safestring import SafeUnicode


_WEEKDAYS = [u'mandag', u'tirsdag', u'onsdag', u'torsdag', u'fredag', u'lørdag', u'søndag']
_MONTHS = [u'januar', u'februar', u'mars', u'april', u'mai', u'juni', u'juli',
           u'august', u'september', u'oktober', u'november', u'desember']


def _format_date(date):
    return '%s %d. %s %s' % (_WEEKDAYS[date.weekday()], date.day, _MONTHS[date.month - 1], date.strftime('%H:%M'))


class Event(models.Model):
    committee_member_percentage = 0.4
    name = models.CharField('navn', max_length=100)
    startdate = models.DateTimeField('startdato')
    enddate = models.DateTimeField('sluttdato')
    has_registration = models.BooleanField(SafeUnicode(u'påmelding'), default=False)
    registration_opens = models.DateTimeField(SafeUnicode(u'påmeldingen åpner'), null=True,
        blank=True)
    registration_closes = models.DateTimeField(SafeUnicode(u'påmeldingen stenger'), null=True,
        blank=True)
    binding_registration = models.BooleanField(SafeUnicode(u'bindende påmelding'), default=False)
    number_of_spots = models.IntegerField('antall plasser', null=True, blank=True,
        help_text='0 = ubegrenset')
    _comittee_registration_opens = models.DateTimeField(SafeUnicode('komitémedlempåmelding åpner'),
        blank=True, null=True, help_text='Når påmeldingen skal åpne for komitémedlemmer. La være'
        ' blank for 24 timer før vanlig åpning.')
    summary = models.TextField('sammendrag')
    description = models.TextField('beskrivelse')
    location = models.CharField('sted', max_length=100)

    class Meta:
        ordering = ['startdate']
        permissions = (
            ('early_signup', 'Can signup to events before regular opening'),
        )

    @property
    def comittee_registration_opens(self):
        if self._comittee_registration_opens:
            return self._comittee_registration_opens
        if self.registration_opens:
            return self.registration_opens - timedelta(days=1)
        return None

    @property
    def number_of_committee_member_spots(self):
        return int(self.number_of_spots*Event.committee_member_percentage)

    def __unicode__(self):
        return self.name

    def to_json(self):
        json = {
            'name': self.name,
            'start_date': self.startdate.isoformat(),
            'end_date': self.enddate.isoformat(),
            'id': self.id,
            'has_registration': self.has_registration,
            'number_of_spots': self.number_of_spots,
            'summary': self.summary,
            'description': self.description,
        }
        if self.has_registration:
            json['registration_opens'] = self.registration_opens.isoformat() if self.registration_opens else None
            json['registration_closes'] = self.registration_closes.isoformat() if self.registration_closes else None
            json['binding_registration'] = self.binding_registration
        return json

    def get_absolute_url(self):
        return reverse('event_detail', kwargs={'event_id': str(self.id)})

    def duration_as_string(self):
        if time.days_between(self.startdate, self.enddate) != 0:
            return 'Fra %s til %s' % (_format_date(time.utc_to_nor(self.startdate)),
                _format_date(time.utc_to_nor(self.enddate)))
        else:
            return 'Fra %s til %s' % (_format_date(time.utc_to_nor(self.startdate)),
                time.utc_to_nor(self.enddate).strftime('%H:%M'))

    def seconds_until_registration_opens_for_user(self, user):
        registration_opens_for_user = self.registration_opens_for_user(user)
        print 'Finding time until opening for user %s' % user
        if self.has_registration and registration_opens_for_user:
            ret = time.seconds_to(registration_opens_for_user)
            print ret
            return ret
        else:
            return 0

    def regular_registration_opens_as_string(self):
        return _format_date(time.utc_to_nor(self.registration_opens))

    def registration_closes_as_string(self):
        return _format_date(time.utc_to_nor(self.registration_closes))

    def is_over(self):
        return time.is_past(self.enddate)

    def is_underway(self):
        return time.is_past(self.startdate) and time.is_future(self.enddate)

    def has_opened(self):
        if self.registration_opens:
            return time.is_past(time.utc_to_nor(self.registration_opens))
        else:
            return True

    def percentage_filled(self):
        num_participants = float(self.num_participants())
        percentage = num_participants / self.number_of_spots * 100
        return int(percentage)

    def num_participants(self):
        return Signup.objects.filter(event=self).count()

    def is_user_participant(self, user):
        if not user.is_authenticated():
            return False
        return Signup.objects.filter(event=self, user=user).exists()

    def registration_opens_for_user(self, user):
        opening_time_for_user = self.registration_opens
        if user and user.has_perm('events.early_signup'):
            opening_time_for_user = self.comittee_registration_opens
        return opening_time_for_user

    def can_user_register_now(self, user):
        if self.registration_opens is None:
            return True
        if self.registration_closes is None:
            opening_time_for_user = self.registration_opens_for_user(user)
            return time.is_past(opening_time_for_user - timedelta(seconds=1))
        else:
            return time.is_past(self.registration_opens) and time.is_future(self.registration_closes)

    def is_registration_closed(self):
        if self.registration_closes is None:
            return False
        return time.is_past(self.registration_closes)

    def is_full(self):
        if self.number_of_spots is None or self.number_of_spots == 0:
            return False
        else:
            return self.num_participants() >= self.number_of_spots

    def is_early_signup_full(self):
        # Add one to check whether adding a user will push us over the 40% limit
        return ((self.num_participants() + 1) / float(self.number_of_spots)) > Event.committee_member_percentage

    def _add_user(self, user):
        Signup.objects.create(event=self, user=user)

    def add_user(self, user):
        """ Add the user to the event, if possible.

        Possible causes if this fails is that the event is not yet open
        for registration, the event is full, or the user is already registered."""

        if not self.can_user_register_now(user):
            raise UserAddError("%s har ikke åpnet for registrering enda, registreringen åpner %s."
                               % (self.name, _format_date(time.utc_to_nor(
                                self.registration_opens_for_user(user)))))
        if (user.has_perm('events.early_signup') and
            time.is_future(self.registration_opens) and self.is_early_signup_full()):
            raise UserAddError('Alle earlybird-plassene til komitémedlemmer er tatt! Du må vente'
                ' til den vanlige påmeldingen starter')
        if self.is_user_participant(user):
            raise UserAddError('Du er allerede påmeldt til %s!' % self.name)
        self._add_user(user)
    add_user.alters_data = True

    def _remove_user(self, user):
        signup = Signup.objects.get(event=self, user=user)
        signup.delete()

    def remove_user(self, user):
        if not self.is_user_participant(user):
            raise NotRegisteredError(event=self, action='Remove user')
        if self.binding_registration:
            raise EventError('You cannot unregister from a binding event!')
        self._remove_user(user)
    remove_user.alters_data = True

    def get_participating_users(self, user_asking=None):
        """ Users with early access should be able to see other people that has signed up after
        the early bird registration has opened, but not before that (admin presignups).

        Normal users should not be able to see any signups until the regular registration opens.
        """
        opening_time = self.registration_opens_for_user(user_asking)
        if opening_time and time.is_future(opening_time):
            return []
        if (not user_asking or
            not user_asking.has_perm('events.early_signup')) and not self.has_opened():
            return []
        signups = Signup.objects.select_related().filter(event=self)
        users = [s.user for s in signups]
        return users

    def get_participating_emails(self):
        users = self.get_participating_users()
        emails = []
        for user in users:
            emails.append(user.email)
        return emails


class EventForm(ModelForm):
    class Meta:
        model = Event
        widgets = {'description': WidgEditorWidget()}
        exclude = []

    def clean_summary(self):
        data = self.cleaned_data['summary']
        clean_data = validate_text(data)
        return clean_data

    def clean_description(self):
        data = self.cleaned_data['description']
        clean_data = validate_text(data)
        return clean_data


class Signup(models.Model):
    event = models.ForeignKey(Event)
    user = models.ForeignKey(User)
    signup_time = models.DateTimeField(SafeUnicode('påmeldingstid'), auto_now=True)

    class Meta:
        ordering = ('event', 'signup_time')


    def __unicode__(self):
        return '%s: %s' % (self.event, self.user)


class EventError(Exception):
    """ Base class for event-related exceptions. """
    pass

class UserAddError(EventError):
    """ Raised if something failed trying to add a user to an event.

    Possible causes might be the event being full, not having opened up
    for registration yet, or the user already being signed up for the event. """

    def __init__(self, reason):
        super(UserAddError, self).__init__()
        self.reason = reason

    def __str__(self):
        return 'Failed to add user to event: %s' % repr(self.reason)

class NotRegisteredError(EventError):
    """ Raised if the user tried to do something one has to be signed up to the event to do."""

    def __init__(self, event, message):
        super(NotRegisteredError, self).__init__()
        self.event = event
        self.message = message

    def __str__(self):
        return 'User is not signed up for %s, so the following could not be performed: %s' % (self.event, self.message)
