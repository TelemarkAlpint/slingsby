from .models import Event

from django.test import Client, TestCase
from datetime import datetime, timedelta

class EventListTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.event = Event.objects.create(name='Testevent', startdate=datetime.now(), has_registration=False,
            binding_registration=False, enddate=(datetime.now() + timedelta(hours=1)))


    def test_get_event_list(self):
        response = self.client.get('/program/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Testevent' in response.content.decode('utf-8'))


    def test_get_event_details(self):
        response = self.client.get('/program/%d/' % self.event.id)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Testevent' in response.content.decode('utf-8'))
