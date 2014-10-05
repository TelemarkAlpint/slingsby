from .models import InstagramMedia, InstagramComment
from .tasks import fetch_instagram_media

import datetime
import json
import os
from mock import patch
from django.test import Client, TestCase

class ResponseMock(object):
    """ Mock a response of `requests.get` """

    def __init__(self, data):
        self.data = data


    def json(self):
        return self.data


def _instagram_recent_media(mock_data):
    def requests_get_mock(*args, **kwargs):
        return ResponseMock(mock_data)
    return requests_get_mock


class InstagramTasksTest(TestCase):

    def test_fetch_instagram_media(self):
        mock_data_path = os.path.join(os.path.dirname(__file__), 'test-data', 'recent_media.json')
        with open(mock_data_path) as fh:
            mock_data = json.load(fh)
        with patch('slingsby.instagram.tasks.requests.get', _instagram_recent_media(mock_data)):
            fetch_instagram_media()
        self.assertEqual(InstagramMedia.objects.count(), 20)
        self.assertEqual(InstagramComment.objects.count(), 33)

        # Set new like count of item 804753730683972274_39861449
        mock_data['data'][0]['likes']['count'] = 1337

        # Test that new runs don't re-add the same stuff, but changes should be saved
        with patch('slingsby.instagram.tasks.requests.get', _instagram_recent_media(mock_data)):
            fetch_instagram_media()
        self.assertEqual(InstagramMedia.objects.count(), 20)
        self.assertEqual(InstagramComment.objects.count(), 33)
        modified_item = InstagramMedia.objects.get(instagram_id="804753730683972274_39861449")
        self.assertEqual(modified_item.like_count, 1337)


class InstagramPageTest(TestCase):

    def setUp(self):
        self.client = Client()
        valid_media = InstagramMedia.objects.create(
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
        InstagramMedia.objects.create(
            media_type='image',
            poster='idiot',
            poster_image='/idiot.png',
            thumbnail_url='/small-idiot.jpg',
            media_url='/nobrains.jpg',
            like_count=0,
            caption='Offensive crap',
            created_time=datetime.datetime.now(),
            instagram_id='notworthy',
            visible=False,
        )
        InstagramComment.objects.create(
            poster='idiot',
            poster_image='/idiot.png',
            text='Stupid shit',
            created_time=datetime.datetime.now(),
            visible=False,
            media=valid_media,
        )


    def test_instagram_page(self):
        response = self.client.get('/instagram/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Snow and awesome stuff' in response.content.decode('utf-8'))
        self.assertFalse('Offensive crap' in response.content.decode('utf-8'))
        self.assertFalse('Stupid shit' in response.content.decode('utf-8'))
