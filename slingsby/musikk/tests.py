# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from .models import Song
from .tasks import process_new_song, get_ssh_client, slugify, get_ssh_connection_params

from django.conf import settings
from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.test.utils import override_settings
from nose.tools import nottest
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
        response = self.client.get('/musikk/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Test song' in response.content.decode('utf-8'))
        self.assertFalse('Not approved' in response.content.decode('utf-8'))


    def test_suggest_song_anon(self):
        response = self.client.post('/musikk/', {'title': 'I Love It', 'artist': 'Icona Pop'})
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
        response = self.client.post('/musikk/', song)
        self.assertEqual(response.status_code, 302)
        admin_response = self.admin_client.get('/musikk/')
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
                response = self.admin_client.post('/musikk/%d/approve/' % self.unapproved_song.id,
                    approval_form)
                processing_mock.delay.assert_called_once()
        os.remove(songfile.name)
        self.assertEqual(response.status_code, 302)
        song_dir = os.path.join(settings.MEDIA_ROOT, 'musikk')
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
        self.fileserver_media_root = '/tmp/fileserver-media-root'


    def tearDown(self):
        shutil.rmtree(self.media_root)


    @needs_ssh
    def test_process_new_song(self):
        with self.settings(MEDIA_ROOT=self.media_root,
                           FILESERVER_MEDIA_ROOT=self.fileserver_media_root):
            process_new_song(self.song.id)
            media_files = os.listdir(os.path.join(settings.MEDIA_ROOT, 'musikk'))
            self.assertTrue('flytta.mp3' in media_files)
            self.assertTrue('flytta.ogg' in media_files)
            fileserver_media_files = _get_fileserver_media_files()
            self.assertTrue('test-artist/approved.mp3' in fileserver_media_files)
            self.assertTrue('test-artist/approved.ogg' in fileserver_media_files)
            # fetch updated song from db
            self.song = Song.objects.first()
            self.assertEqual(str(self.song.filename), 'musikk/test-artist/approved')
            self.assertTrue(self.song.ready)


def _get_fileserver_media_files():
    ssh_client = get_ssh_client()
    music_dir = settings.FILESERVER_MEDIA_ROOT + '/musikk'
    stdout = ssh_client.exec_command('find %s' % music_dir)[1]
    output = stdout.read()
    output_lines = output.split()
    # Strip paths like /tmp/filserver_media_dir/musikk/artist/song.mp3 to musikk/artist/song.mp3
    clean_lines = [path[len(music_dir):].lstrip('/') for path in output_lines]
    ssh_client.exec_command('rm -rf %s' % music_dir)
    return clean_lines


class UtilTest(TestCase):

    def test_slugify(self):
        tests = (
            ("I love it'", 'i-love-it'),
            ("J'ai parlée français, un peu", 'jai-parlee-francais-un-peu'),
            ("Åge og sambandet e hærlig, sjø!, ", 'age-og-sambandet-e-haerlig-sjo'),
        )
        for value, expected in tests:
            self.assertEqual(slugify(value), expected)


    def test_get_connection_params(self):
        tests = [
            ('localhost', ('vagrant', 'localhost', 22)),
            ('vagrant@localhost:22', ('vagrant', 'localhost', 22)),
            ('travis@127.0.0.1:2222', ('travis', '127.0.0.1', 2222)),
        ]
        for connection_string, expected_result in tests:
            result = get_ssh_connection_params(connection_string)
            self.assertEqual(result, expected_result)
