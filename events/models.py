# coding: utf-8

from django.contrib.auth.models import User
from django.db import models
from django.db.models import permalink
from django.db.models.signals import post_save
from django.forms.models import ModelForm
from django.utils.safestring import SafeUnicode
from django.views.generic.list import ListView
from general import time, validate_text, make_title
from general.cache import CachedQuery
from general.widgets import WidgEditorWidget

_COUNTDOWN_TIME_IN_S = 1800
_WEEKDAYS = [u'mandag', u'tirsdag', u'onsdag', u'torsdag', u'fredag', u'lørdag', u'søndag']
_MONTHS =  [u'januar', u'februar', u'mars', u'april', u'mai', u'juni', u'juli',
            u'august', u'september', u'oktober', u'november', u'desember']

class Event(models.Model):
    name = models.CharField('navn', max_length=100)
    startdate = models.DateTimeField('startdao')
    enddate = models.DateTimeField('sluttdato')
    has_registration = models.BooleanField(SafeUnicode(u'påmelding'))
    registration_opens = models.DateTimeField(SafeUnicode(u'påmeldingen åpner'), null=True, blank=True)
    registration_closes = models.DateTimeField(SafeUnicode(u'påmeldingen stenger'), null=True, blank=True)
    binding_registration = models.BooleanField(SafeUnicode(u'bindende påmelding'))
    number_of_spots = models.IntegerField('antall plasser', null=True, blank=True, help_text='0 = ubegrenset')
    participants_by_id = models.CommaSeparatedIntegerField('deltager-IDer', max_length=4000, null=True, blank=True)
    summary = models.TextField('sammendrag')
    description = models.TextField('beskrivelse')
    location = models.CharField('sted', max_length=100)

    class Meta:
        ordering = ['startdate']

    def __unicode__(self):
        return self.name

    def __json__(self):
        fields = {
                'name': self.name,
                'start_date': self.startdate.isoformat(),
                'end_date': self.enddate.isoformat(),
                'id': self.id,
                'has_registration': self.has_registration,
                'number_of_spots': self.number_of_spots,
        }
        if self.has_registration:
            fields['registration_opens'] = self.registration_opens.isoformat() if self.registration_opens else None
            fields['registration_closes'] = self.registration_closes.isoformat() if self.registration_closes else None
            fields['binding_registration'] = self.binding_registration
        return fields

    @permalink
    def get_absolute_url(self):
        return ('events.views.detail', [str(self.id)])

    def duration_as_string(self):
        if time.days_between(self.startdate, self.enddate) != 0:
            return 'Fra %s til %s' % (self._format_date(self.startdate), self._format_date(self.enddate))
        else:
            return 'Fra %s til %s' % (self._format_date(self.startdate), self.enddate.strftime('%H:%M'))

    def _format_date(self, date):
        return '%s %d. %s %s' % (_WEEKDAYS[date.weekday()], date.day, _MONTHS[date.month - 1], date.strftime('%H:%M'))

    def registration_closes_as_string(self):
        return self._format_date(self.registration_closes)

    def registration_opens_as_string(self):
        return self._format_date(self.registration_opens)

    def is_over(self):
        return time.is_past(self.enddate)

    def is_underway(self):
        return time.is_past(self.startdate) and time.is_future(self.enddate)

    def has_opened(self):
        if self.registration_opens:
            return time.is_past(self.registration_opens)
        else:
            return True

    def percentage_filled(self):
        num_participants = float(self.num_participants())
        percentage = num_participants / self.number_of_spots * 100
        return int(percentage)

    def num_participants(self):
        return len(self.get_participants_id())

    def is_user_participant(self, user):
        return user.id in self.get_participants_id()

    def is_open_for_registration(self):
        if self.registration_opens is None:
            return True
        if self.registration_closes is None:
            return time.is_past(self.registration_opens)
        else:
            return time.is_past(self.registration_opens) and time.is_future(self.registration_closes)

    def is_registration_closed(self):
        if self.registration_closes is None:
            return False
        return time.is_past(self.registration_closes)

    def is_full(self):
        if self.number_of_spots == 0:
            return False
        else:
            return self.num_participants() >= self.number_of_spots

    def use_countdown(self):
        if self.registration_opens:
            return 0 < time.seconds_to(self.registration_opens) < _COUNTDOWN_TIME_IN_S
        else:
            return False

    def seconds_to_registration_opening(self):
        seconds = max(time.seconds_to(self.registration_opens), 0)
        return seconds

    def add_user(self, user):
        if self.is_full():
            raise EventFullException('%s tried to register to the event %s, which is full.' % (user, self))
        if self.is_user_participant(user):
            raise UserAlreadyRegisteredException('''%s tried to register to the event %s, which he is already
                                                    participating''' % (user, self))
        participants = self.get_participants_id()
        participants.append(user.id)
        self.update_participating_users(participants)
    add_user.alters_data = True

    def remove_user(self, user):
        if self.is_user_participant(user):
            participants = self.get_participants_id()
            participants.remove(user.id)
            self.update_participating_users(participants)
    remove_user.alters_data = True

    def get_participants_id(self):
        user_ids = []
        if self.participants_by_id:
            user_ids = map(int, self.participants_by_id.split(','))
        return user_ids

    def get_id(self):
        return int(self.id)

    def get_participating_users(self):
        if not self.has_opened():
            return []
        user_ids = self.get_participants_id()
        users = [User.objects.get(id=user_id) for user_id in user_ids]
        return users

    def update_participating_users(self, list_of_new_ids):
        list_of_new_ids = map(str, list_of_new_ids)
        self.participants_by_id = ','.join(list_of_new_ids)
        self.save()
    update_participating_users.alters_data = True

    def get_participating_emails(self):
        users = self.get_participating_users()
        emails = []
        for user in users:
            emails.append(user.email)
        return emails

class NextEventsQuery(CachedQuery):
    keyword = 'next_events'
    queryset = Event.objects.filter(startdate__gte=time.now())[:3]
    timeout_in_s = 3600
post_save.connect(NextEventsQuery.empty_on_save, sender=Event)

class EventForm(ModelForm):
    class Meta:
        model = Event
        widgets = {'description': WidgEditorWidget()}

    def clean_summary(self):
        data = self.cleaned_data['summary']
        clean_data = validate_text(data)
        return clean_data

    def clean_description(self):
        data = self.cleaned_data['description']
        clean_data = validate_text(data)
        return clean_data

class EventListView(ListView):
    model = Event
    context_object_name = 'event_list'
    template_name = 'events/event_list.html'
    paginate_by = 5

    def get_queryset(self):
        raw_events = Event.objects.filter(startdate__gte=time.now())
        events = [event for event in raw_events if time.is_future(event.enddate)]
        return events

    def get_context_data(self, **kwargs):
        context = super(EventListView, self).get_context_data(**kwargs)
        context['title'] = make_title('Program')
        return context

class EventFullException(Exception):
    pass

class UserAlreadyRegisteredException(Exception):
    pass

