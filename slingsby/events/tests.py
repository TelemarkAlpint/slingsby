from .models import Event

from django.test import Client, TestCase
from django.contrib.auth.models import User
from datetime import datetime, timedelta

class BasicEventTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.event = Event.objects.create(name='Testevent', startdate=datetime.now(), has_registration=False,
            binding_registration=False, enddate=(datetime.now() + timedelta(hours=1)))


    def test_get_event_list(self):
        response = self.client.get('/program')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Testevent' in response.content.decode('utf-8'))


    def test_get_event_details(self):
        response = self.client.get('/program/%d' % self.event.id)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Testevent' in response.content.decode('utf-8'))


class EventWithoutSignupOpenTimeTest(TestCase):

    def setUp(self):
        self.client = Client()
        User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.event = Event.objects.create(name='Testevent', startdate=datetime.now(), has_registration=True,
            binding_registration=False, enddate=(datetime.now() + timedelta(hours=1)))


    def test_join_event_without_signup_open_time(self):
        # No signup time should just imply that the event is open for signup immediately
        response = self.client.post('/program/1/join')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(Event.objects.first().get_participating_users()), 1)


    def test_show_event_without_signup_open_time(self):
        response = self.client.get('/program/1')
        self.assertEqual(response.status_code, 200)


class EventSignupTest(TestCase):

    def setUp(self):
        self.anon_user = Client()
        self.logged_in_user = Client()
        User.objects.create_user(username='joe', password='joespw')
        self.logged_in_user.login(username='joe', password='joespw')
        self.no_signup_event = Event.objects.create(name='Skifestivalen',
            startdate=(datetime.now() + timedelta(days=3)), enddate=(datetime.now() +
                timedelta(days=3, hours=5))
        self.
