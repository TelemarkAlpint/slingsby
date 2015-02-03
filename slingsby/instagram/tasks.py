# -*- coding: utf-8 -*-

from ..general.utils import log_errors
from .models import InstagramMedia, InstagramComment

import requests
from celery import shared_task
from datetime import datetime
from django.conf import settings
from logging import getLogger


_logger = getLogger('slingsby.musikk.tasks')


def load_media_from_instagram_response(json_data):
    """ Loads new media from the data provided, and detects changes like comments deleted
    and new likes.
    """
    for media in json_data['data']:
        media_key = 'videos' if media['type'] == 'video' else 'images'
        instagram_media, created = InstagramMedia.objects.get_or_create(
            instagram_id=media['id'],
            defaults={
                'media_type': media['type'],
                'thumbnail_url': media['images']['thumbnail']['url'],
                'media_url': media[media_key]['standard_resolution']['url'],
                'visible': True,
                'created_time': datetime.utcfromtimestamp(float(media['created_time'])),
            }
        )
        instagram_media.like_count = media['likes']['count']
        # Not all images have captions
        instagram_media.caption = media['caption']['text'] if media['caption'] else ''
        instagram_media.poster = media['user']['username']
        instagram_media.poster_image = media['user']['profile_picture']
        instagram_media.save()
        if created:
            _logger.info('New instagram media added (%s): %s', instagram_media.instagram_id,
                instagram_media.caption)
        for comment in media['comments']['data']:
            instagram_comment, comment_created = InstagramComment.objects.get_or_create(
                instagram_id=comment['id'],
                defaults={
                    'poster': comment['from']['username'],
                    'poster_image': comment['from']['profile_picture'],
                    'created_time': datetime.utcfromtimestamp(float(comment['created_time'])),
                    'text': comment['text'],
                    'media': instagram_media,
                }
            )
            if comment_created:
                _logger.info('New comment to %s added (%s): %s', instagram_media.instagram_id,
                    instagram_comment.instagram_id, instagram_comment.text)


@shared_task
@log_errors
def fetch_instagram_media():
    _logger.info('Fetching media from instagram')
    recent_media = requests.get('https://api.instagram.com/v1/tags/ntnuita/media/recent',
        params={'client_id': settings.INSTAGRAM_CLIENT_ID}).json()
    load_media_from_instagram_response(recent_media)
