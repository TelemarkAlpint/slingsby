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
        instagram_media = InstagramMedia()
        instagram_media.media_type = media['type']
        instagram_media.poster = media['user']['username']
        instagram_media.poster_image = media['user']['profile_picture']
        instagram_media.thumbnail_url = media['images']['thumbnail']['url']
        if instagram_media.media_type == 'video':
            instagram_media.media_url = media['videos']['standard_resolution']['url']
        else:
            instagram_media.media_url = media['images']['standard_resolution']['url']
        instagram_media.like_count = media['likes']['count']
        instagram_media.caption = media['caption']['text']
        instagram_media.created_time = datetime.datetime.utcfromtimestamp(float(media['created_time']))
        instagram_media.instagram_id = media['id']
        instagram_media.save()
        for comment in media['comments']['data']:
            instagram_comment = InstagramComment()
            instagram_comment.poster = comment['from']['username']
            instagram_comment.poster_image = comment['from']['profile_picture']
            instagram_comment.created_time = datetime.datetime.utcfromtimestamp(float(comment['created_time']))
            instagram_comment.instagram_id = comment['id']
            instagram_comment.text = comment['text']
            instagram_comment.media = instagram_media
            instagram_comment.save()
