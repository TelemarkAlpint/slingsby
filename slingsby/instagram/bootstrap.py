from .models import InstagramMedia, InstagramComment

import datetime
import json
import os

def bootstrap():
    recent_media_path = os.path.join(os.path.dirname(__file__), 'test-data', 'recent_media.json')
    with open(recent_media_path) as fh:
        recent_media = json.load(fh)
        for media in recent_media['data']:
            type_plural = 'videos' if media['type'] == 'video' else 'images'
            instagram_media, created = InstagramMedia.objects.get_or_create(
                media_type=media['type'],
                poster=media['user']['username'],
                poster_image=media['user']['profile_picture'],
                thumbnail_url=media['images']['thumbnail']['url'],
                media_url=media[type_plural]['standard_resolution']['url'],
                like_count=media['likes']['count'],
                caption=media['caption']['text'],
                created_time=datetime.datetime.utcfromtimestamp(float(media['created_time'])),
                instagram_id=media['id'],
            )
            for comment in media['comments']['data']:
                InstagramComment.objects.get_or_create(
                    poster=comment['from']['username'],
                    poster_image=comment['from']['profile_picture'],
                    created_time=datetime.datetime.utcfromtimestamp(float(comment['created_time'])),
                    instagram_id=comment['id'],
                    text=comment['text'],
                    media=instagram_media,
                )
