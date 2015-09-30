# -*- coding: utf-8 -*-

from .models import Event, Signup

from django.test import Client, TestCase
from django.contrib.auth.models import User, Group, Permission
from datetime import datetime, timedelta

class BasicEventTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.event = Event.objects.create(name='Testevent', startdate=datetime.now(),
            enddate=(datetime.now() + timedelta(hours=1)))


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
        self.logged_in_user1 = Client()
        self.logged_in_user2 = Client()
        joe = User.objects.create_user(username='joe', password='joespw')
        self.knut = User.objects.create_user(username='knut', password='knutspw')
        arrkom = Group.objects.create(name='Arrkom')
        arrkom.permissions.add(Permission.objects.get(codename='early_signup'))
        self.knut.groups.add(arrkom)
        self.logged_in_user1.login(username='joe', password='joespw')
        self.logged_in_user2.login(username='knut', password='knutspw')
        self.no_signup_time_event = Event.objects.create(name='Testevent',
            startdate=(datetime.now() + timedelta(days=3)), enddate=(datetime.now() +
                timedelta(days=3, hours=5)), has_registration=True)
        self.single_spot_event = Event.objects.create(name='Testevent',
            startdate=(datetime.now() + timedelta(days=1)), enddate=(datetime.now() +
                timedelta(days=2)), has_registration=True, registration_opens=(datetime.now() -
                timedelta(minutes=10)), number_of_spots=1)
        self.event_with_presignups = Event.objects.create(name='Other testevent',
            startdate=(datetime.now() + timedelta(days=3)), registration_opens=(datetime.now() +
                timedelta(days=2)), has_registration=True, enddate=(datetime.now() + timedelta(days=4)))
        self.event_with_presignups._add_user(joe)


    def test_event_hides_presignups(self):
        self.assertEqual(self.event_with_presignups.get_participating_users(), [])
        self.assertEqual(self.event_with_presignups.get_participating_users(self.knut), [])


    def test_event_unregister(self):
        event_id = self.event_with_presignups.id
        response = self.logged_in_user1.post('/program/%d/leave' % event_id)
        self.assertEqual(response.status_code, 302)
        self.assertTrue('/program/%d' % event_id in response.get('location'))

        self.assertEqual(Signup.objects.count(), 0)


    def test_event_signup_logged_in_only(self):
        response = self.anon_user.post('/program/1/join')
        # Non-authenticated requests should redirect to logged_in_user
        self.assertEqual(response.status_code, 302)
        self.assertTrue('/login' in response.get('location'))

        response = self.logged_in_user1.post('/program/1/join')
        self.assertEqual(response.status_code, 302)
        self.assertTrue('/program/1' in response.get('location'))


    def test_waiting_list(self):
        response = self.logged_in_user1.post('/program/2/join', follow=True)
        self.assertContains(response, 'joe')
        self.assertNotContains(response, 'Venteliste')

        response = self.logged_in_user2.post('/program/2/join', follow=True)
        self.assertContains(response, 'knut')
        self.assertContains(response, 'Venteliste')


class EventSignupCommitteeTest(TestCase):

    def setUp(self):
        self.anon_user = Client()
        self.logged_in_user = Client()
        self.committee_member1 = Client()
        self.committee_member2 = Client()
        User.objects.create_user(username='joe', password='joespw')
        committee_member1 = User.objects.create_user(username='arnulf', password='arnulfspw')
        committee_member2 = User.objects.create_user(username='øverland', password='øverlandspw')
        arrkom = Group.objects.create(name='Arrkom')
        arrkom.permissions.add(Permission.objects.get(codename='early_signup'))
        committee_member1.groups.add(arrkom)
        committee_member2.groups.add(arrkom)
        self.logged_in_user.login(username='joe', password='joespw')
        self.committee_member1.login(username='arnulf', password='arnulfspw')
        self.committee_member2.login(username='øverland', password='øverlandspw')
        self.event = Event.objects.create(name='Testevent',
            startdate=(datetime.now() + timedelta(days=3)), enddate=(datetime.now() +
                timedelta(days=3, hours=5)), has_registration=True, number_of_spots=3,
            registration_opens=(datetime.now() + timedelta(days=1)),
            registration_closes=(datetime.now() + timedelta(days=2)),
            _comittee_registration_opens=(datetime.now() - timedelta(hours=2)))


    def test_event_signup_for_committee_members(self):
        response = self.anon_user.get('/program/1')
        self.assertEqual(response.status_code, 200)
        response = self.anon_user.post('/program/1/join')
        # Non-authenticated requests should redirect to logged_in_user
        self.assertEqual(response.status_code, 302)
        self.assertTrue('/login' in response.get('location'))

        response = self.logged_in_user.get('/program/1')
        self.assertEqual(response.status_code, 200)
        response = self.logged_in_user.post('/program/1/join')
        self.assertEqual(response.status_code, 400)

        response = self.committee_member1.get('/program/1')
        self.assertEqual(response.status_code, 200)
        response = self.committee_member1.post('/program/1/join')
        self.assertEqual(response.status_code, 302)
        self.assertTrue('/program/1' in response.get('location'))
        self.assertEqual(self.event.num_participants(), 1)

        # Should reject early signups if total percentage becomes more than 40%
        response = self.committee_member2.post('/program/1/join')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.event.num_participants(), 1)

        # If earlybird is full, committee members should have countdown to normal signup
        self.assertTrue(self.event.signup_countdown_seconds(
            User.objects.get(username='øverland')) > 0)

        # øverland should see the single comittee member signup
        self.assertEqual(len(self.event.get_participating_users(
            User.objects.get(username='øverland'))), 1)

        # normal users should not see any signups
        self.assertEqual(len(self.event.get_participating_users(
            User.objects.get(username='joe'))), 0)
        self.assertEqual(len(self.event.get_participating_users()), 0)
