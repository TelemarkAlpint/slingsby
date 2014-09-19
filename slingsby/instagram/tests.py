from .models import InstagramMedia, InstagramComment
from .tasks import fetch_instagram_media

import datetime
import json
import os
from mock import patch
from django.test import Client, TestCase

class ResponseMock(object):

    def __init__(self, data):
        self.data = data


    def json(self):
        return self.data


def _instagram_recent_media(*args, **kwargs):
    mock_data = os.path.join(os.path.dirname(__file__), 'test-data', 'recent_media.json')
    with open(mock_data) as fh:
        return ResponseMock(json.load(fh))


class InstagramTasksTest(TestCase):

    def test_fetch_instagram_media(self):
        with patch('slingsby.instagram.tasks.requests.get', _instagram_recent_media):
            fetch_instagram_media()
        self.assertEqual(InstagramMedia.objects.count(), 20)
        self.assertEqual(InstagramComment.objects.count(), 33)

class InstagramPageTest(TestCase):

    def setUp(self):
        self.client = Client()
        InstagramMedia.objects.create(
            media_type='image',
            poster='ntnuitaadmin',
            poster_image='/admin.png',
            thumbnail_url='/thumb.jpg',
            media_url='/fullsize.jpg',
            like_count=1337,
            caption='Snow and awesome stuff this weekend with #ntnuita',
            created_time=datetime.datetime.now(),
            instagram_id='cafed00d',
        )


    def test_instagram_page(self):
        response = self.client.get('/instagram/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Snow and awesome stuff' in response.content.decode('utf-8'))
