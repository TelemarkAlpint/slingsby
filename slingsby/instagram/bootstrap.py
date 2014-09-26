from .models import InstagramMedia, InstagramComment
from .tasks import load_media_from_instagram_response

import datetime
import json
import os

def bootstrap():
    recent_media_path = os.path.join(os.path.dirname(__file__), 'test-data', 'recent_media.json')
    with open(recent_media_path) as fh:
        recent_media = json.load(fh)
        load_media_from_instagram_response(recent_media)
