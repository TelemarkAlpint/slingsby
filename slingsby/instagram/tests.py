from .models import InstagramMedia, InstagramComment
from .tasks import fetch_instagram_media

import os
import json
from mock import patch
from django.test import TestCase

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
