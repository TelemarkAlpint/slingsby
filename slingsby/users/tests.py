# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from .tasks import demote_inactive_users

from django.test import Client, TestCase
from django.utils import timezone
from django.contrib.messages.storage.cookie import CookieStorage
from django.core import mail
from django.contrib.auth.models import User
import datetime
import re


class ProfilePageTest(TestCase):

    def setUp(self):
        self.anon_user = Client()
        self.logged_in_user = Client()
        User.objects.create_user(username='testuser', password='testpassword')
        self.logged_in_user.login(username='testuser', password='testpassword')


    def test_profile_page(self):
        anon_response = self.anon_user.get('/profil')
        self.assertEqual(anon_response.status_code, 302)

        auth_response = self.logged_in_user.get('/profil')
        self.assertEqual(auth_response.status_code, 200)


class SignupTest(TestCase):

    def setUp(self):
        self.logged_in_user = Client()
        User.objects.create_user(username='testuser', password='password')
        self.logged_in_user.login(username='testuser', password='password')

        self.member = Client()
        member = User.objects.create_user(username='member', password='password')
        member.profile.member_since = timezone.now()
        member.profile.save()
        self.member.login(username='member', password='password')


    def test_get_signup_page(self):
        response = self.logged_in_user.get('/blimed')
        self.assertEqual(response.status_code, 200)


    def test_invalid_email_signup(self):
        response = self.logged_in_user.post('/blimed', {'email': 'invalid'})
        self.assertEqual(response.status_code, 400)


    def test_correct_signup_flow(self):
        response = self.logged_in_user.post('/blimed', {'email': 'testuser@testdomain.com'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response['location'].endswith('/profil'))

        # test that mail was sent
        self.assertEqual(len(mail.outbox), 1)
        challenge_mail = mail.outbox[0]
        self.assertEqual(len(challenge_mail.alternatives), 1)
        content, content_type = challenge_mail.alternatives[0]
        self.assertEqual(content_type, 'text/html')

        # Test that user can complete flow with token
        token_re = re.compile(r'\?token=([0-9a-zA-Z]*)')
        token_sent = token_re.search(challenge_mail.body).groups()[0]
        response = self.logged_in_user.get('/profil?token=' + token_sent)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response['location'].endswith('/profil'))
        user = User.objects.get(username='testuser')
        self.assertTrue(user.profile.email_confirmed_at is not None)


    def test_members_are_redirected(self):
        response = self.member.get('/blimed')
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response['location'].endswith('/profil'))


class InvalidSignupFlowTest(TestCase):

    def setUp(self):
        User.objects.create_user(username='testuser', password='password')
        self.logged_in_user = Client()
        self.logged_in_user.login(username='testuser', password='password')
        self.user = User.objects.get(username='testuser')
        self.user.profile.email_challenge = 'secret'
        self.user.profile.email_token_expiration_date = (timezone.now()
            + datetime.timedelta(hours=48))
        self.user.profile.save()

    def _get_messages(self, response):
        messages = CookieStorage(response)._decode(response.cookies['messages'].value) # pylint: disable=protected-access
        return [m.message for m in messages]


    def test_invalid_token(self):
        response = self.logged_in_user.get('/profil?token=secrt')
        self.assertEqual(response.status_code, 400)


    def test_expired_token(self):
        self.user.profile.email_token_expiration_date = (timezone.now()
            - datetime.timedelta(hours=1))
        self.user.profile.save()

        response = self.logged_in_user.get('/profil?token=secret')
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response['location'].endswith('/profil'))
        messages = self._get_messages(response)
        self.assertEqual(len(messages), 1)
        self.assertTrue(any('utløpt' in m for m in messages))


    def test_submitting_token_twice(self):
        response = self.logged_in_user.get('/profil?token=secret')
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response['location'].endswith('/profil'))

        response = self.logged_in_user.get('/profil?token=secret')
        self.assertEqual(response.status_code, 302)
        messages = self._get_messages(response)
        self.assertTrue(any('allerede bekreftet' in m for m in messages))
        # from nose.tools import set_trace as f; f()


class InactiveUserDemotionTest(TestCase):

    def setUp(self):
        active_user = User.objects.create(username='active', password='pw')
        active_user.profile.member_since = timezone.now()
        active_user.profile.save()
        active_user.last_login = timezone.now() - datetime.timedelta(days=10)
        active_user.save()

        inactive_user = User.objects.create(username='inactive', password='pw')
        inactive_user.profile.member_since = timezone.now()
        inactive_user.profile.save()
        inactive_user.last_login = timezone.now() - datetime.timedelta(days=400)
        inactive_user.save()


    def test_inactive_user_demoted_from_active(self):
        demote_inactive_users()

        # Inactive user should have been demoted from member status
        inactive_user = User.objects.get(username='inactive')
        self.assertFalse(inactive_user.profile.member_since)

        # Active user should be unaffected
        active_user = User.objects.get(username='active')
        self.assertTrue(active_user.profile.member_since)


class DevLoginTest(TestCase):

    def test_devlogin_in_dev_only(self):
        response = self.client.get('/devlogin')
        self.assertEqual(response.status_code, 404)
