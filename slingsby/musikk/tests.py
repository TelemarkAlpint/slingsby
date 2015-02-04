# -*- coding: utf-8 -*-

from .models import Song, Vote
from .tasks import process_new_song, count_votes

from django.conf import settings
from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.test.utils import override_settings
from nose.tools import nottest
import datetime
import mock
import os
import shutil
import tempfile


def needs_ssh(func):
    """ Decorator for tests that should only be run if a SSH client is
    available (ie RUN_SSH_TESTS=1).
    """
    if os.environ.get('RUN_SSH_TESTS', False):
        return func
    else:
        return nottest(func)


class SongListTest(TestCase):

    def setUp(self):
        self.client = Client()
        Song.objects.create(title='Test song', artist='Test artist', ready=True)
        Song.objects.create(title='Not approved yet', artist='Test artist', ready=False)


    def test_get_song_list(self):
        response = self.client.get('/musikk')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Test song' in response.content.decode('utf-8'))
        self.assertFalse('Not approved' in response.content.decode('utf-8'))


    def test_suggest_song_anon(self):
        response = self.client.post('/musikk', {'title': 'I Love It', 'artist': 'Icona Pop'})
        self.assertEqual(response.status_code, 401)


class AuthenticatedSongTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin_client = Client()
        User.objects.create_user(username='testuser', password='testpassword')
        adminuser = User.objects.create_user(username='testadmin', password='adminpw')
        adminuser.is_staff = True
        adminuser.is_superuser = True
        adminuser.save()
        self.client.login(username='testuser', password='testpassword')
        self.admin_client.login(username='testadmin', password='adminpw')
        self.unapproved_song = Song.objects.create(title='Not approved yet', artist='Test artist', ready=False)


    def test_suggest_song(self):
        song = {
            'title': 'I Love It',
            'artist': 'Icona Pop',
            'startpoint_in_s': 0,
        }
        response = self.client.post('/musikk', song)
        self.assertEqual(response.status_code, 302)
        admin_response = self.admin_client.get('/musikk')
        self.assertEqual(admin_response.status_code, 200)
        self.assertTrue('I Love It' in admin_response.content.decode('utf-8'))


    @override_settings(MEDIA_ROOT=tempfile.mkdtemp())
    def test_approve_song(self):
        songfile = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
        songfile.write('mysong')
        songfile.close()
        with open(songfile.name) as song_fh:
            approval_form = {
                'filename': song_fh,
                'title': 'Approved',
                'artist': 'Approved artist',
                'startpoint_in_s': 0,
            }
            processing_mock = mock.MagicMock()
            with mock.patch('slingsby.musikk.views.process_new_song', processing_mock):
                response = self.admin_client.post('/musikk/%d/approve' % self.unapproved_song.id,
                    approval_form)
                processing_mock.delay.assert_called_once()
        os.remove(songfile.name)
        self.assertEqual(response.status_code, 302)
        song_dir = os.path.join(settings.MEDIA_ROOT, 'local', 'musikk')
        uploaded_song = os.path.join(song_dir, os.listdir(song_dir)[0])
        with open(uploaded_song) as song_fh:
            self.assertEqual(song_fh.read(), 'mysong')
        shutil.rmtree(song_dir)
        song = Song.objects.first()
        self.assertEqual(song.title, 'Approved')
        self.assertEqual(song.artist, 'Approved artist')
        # Should not be ready yet (needs to be uploaded to fileserver first)
        self.assertFalse(song.ready)




class SongTasksTest(TestCase):

    def setUp(self):
        this_dir = os.path.dirname(__file__)
        raw_song_file = os.path.abspath(os.path.join(this_dir, 'test-data', 'flytta-raw.flac'))
        self.song = Song.objects.create(title='Approved', artist='Test artist', ready=False,
            filename=raw_song_file)
        self.media_root = tempfile.mkdtemp()
        self.external_media_root = os.path.join(self.media_root, 'external')


    def tearDown(self):
        shutil.rmtree(self.media_root)


    @needs_ssh
    def test_process_new_song(self):
        with self.settings(MEDIA_ROOT=self.media_root, SSH_CLIENT=None,
            EXTERNAL_MEDIA_ROOT=self.external_media_root):
            process_new_song(self.song.id)
            media_files = os.listdir(os.path.join(settings.EXTERNAL_MEDIA_ROOT, 'musikk',
                'test-artist'))
            self.assertTrue('approved.mp3' in media_files)
            self.assertTrue('approved.ogg' in media_files)

            # fetch updated song from db
            self.song = Song.objects.first()
            self.assertEqual(str(self.song.filename), 'musikk/test-artist/approved')
            self.assertTrue(self.song.ready)


class SongActionsTest(TestCase):

    def setUp(self):
        self.client = Client()
        User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.song = Song.objects.create(title='I Love It', artist='Icona Pop', ready=True,
            filename='iloveit')


    def test_vote_on_song(self):
        with mock.patch('slingsby.musikk.views.count_votes') as count_votes_mock:
            response = self.client.post('/musikk/%d/vote' % self.song.id)
            count_votes_mock.delay.assert_called_once()
        self.assertEqual(response.status_code, 200)
        num_votes = Vote.objects.count()
        self.assertEqual(num_votes, 1)


class TopSongsTest(TestCase):

    def setUp(self):
        self.client = Client()


    def test_top_musikk_pages(self):
        requests_mock = mock.Mock()
        requests_mock.get.return_value.json.return_value = {
            'last_updated': datetime.datetime.now().strftime("%d.%m.%y %H:%M"),
            'url': '/popular-song',
        }
        with mock.patch('slingsby.musikk.views.requests', requests_mock):
            response = self.client.get('/musikk/top')
            self.assertEqual(response.status_code, 200)

            response = self.client.get('/musikk/top/song')
            self.assertEqual(response.status_code, 302)

        response = self.client.get('/musikk/top/list')
        self.assertEqual(response.status_code, 200)



class VoteCountTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.iloveit = Song.objects.create(title='I Love It', artist='Icona Pop', ready=True,
            filename='iloveit')
        self.hammertime = Song.objects.create(title="U Can't Touch This", artist='MC Hammer', ready=True,
            filename='canttouchthis')
        Vote.objects.create(song=self.hammertime, user=self.user)


    def test_count_votes(self):
        count_votes()
        hammertime = Song.objects.get(pk=self.hammertime.id)
        iloveit = Song.objects.get(pk=self.iloveit.id)
        self.assertEqual(hammertime.popularity, 100)
        self.assertEqual(iloveit.popularity, 0)
        Vote.objects.create(song=iloveit, user=self.user)
        count_votes()
        hammertime = Song.objects.get(pk=self.hammertime.id)
        iloveit = Song.objects.get(pk=self.iloveit.id)
        self.assertTrue(iloveit.popularity > hammertime.popularity)
