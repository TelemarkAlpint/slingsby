# -*- coding: utf-8 -*-

from .models import InstagramMedia, InstagramComment

import requests
import datetime
from celery import shared_task
from django.conf import settings
from functools import wraps
from logging import getLogger


_logger = getLogger('slingsby.musikk.tasks')


def log_errors(func):
    """ Decorator to wrap a function in a try/except, and log errors. """

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except: # pylint: disable=bare-except
            _logger.exception("Task failed!")

    return wrapper


@shared_task
@log_errors
def fetch_instagram_media():
    """ Takes a raw song uploaded (assumed to be FLAC), converts it into mp3 and ogg,
    pushes it to the fileserver, and updates the song filename and marks it as ready.
    """
    _logger.info('Fetching media from instagram')
    recent_media = requests.get('https://api.instagram.com/v1/tags/ntnuita/media/recent',
        params={'client_id': settings.INSTAGRAM_CLIENT_ID}).json()
    for media in recent_media['data']:
        instagram_media, created = InstagramMedia.objects.get_or_create(
            instagram_id=media['id'],
            defaults={
                'media_type': media['type'],
                'poster': media['user']['username'],
                'poster_image': media['user']['profile_picture'],
                'thumbnail_url': media['images']['thumbnail']['url'],
                'media_url': media['videos' if media['type'] == 'video' else 'images']['standard_resolution']['url'],
                'like_count': media['likes']['count'],
                'caption': media['caption']['text'],
                'created_time': datetime.datetime.utcfromtimestamp(float(media['created_time'])),
            }
        )
        for comment in media['comments']['data']:
            InstagramComment.objects.get_or_create(
                instagram_id=comment['id'],
                defaults={
                    'poster': comment['from']['username'],
                    'poster_image': comment['from']['profile_picture'],
                    'created_time': datetime.datetime.utcfromtimestamp(float(comment['created_time'])),
                    'text': comment['text'],
                    'media': instagram_media,
                }
            )
