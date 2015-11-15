from .models import Song

from django.conf import settings
from django.utils.lorem_ipsum import words
import random
import shutil
import os

def bootstrap():
    # Create some songs on the toplist
    Song.objects.get_or_create(title='Danger Zone',
        artist='Kenny Loggins',
        popularity=30,
        ready=True,
    )
    Song.objects.get_or_create(title='Radioactive',
        artist='Imagine Dragons',
        ready=True,
        votes=2,
    )
    Song.objects.get_or_create(title='Better Off Alone',
        artist='Alice Deejay',
        popularity=50,
        votes=3,
        ready=True,
    )

    # Put a converted song in external media for playback
    source_file = os.path.join(os.path.dirname(__file__), 'test-data', 'flytta.mp3')
    music_dir = os.path.join(settings.MEDIA_ROOT, 'musikk')
    create_target_directory_and_copy(source_file, os.path.join(music_dir, 'compilations', 'latest.mp3'))
    create_target_directory_and_copy(source_file, os.path.join(music_dir, 'alina-devecerski', 'flytta.mp3'))

    # Create some random filler songs
    for i in range(41):
        Song.objects.get_or_create(
            artist='Artist %d' % i,
            ready=True,
            defaults={
                'popularity': random.randint(0, 100),
                'title': ' '.join(random.sample(words(40).split(), random.randint(2, 5))).title(),
            }
        )


    # Create some new song suggestions
    Song.objects.get_or_create(title='The Bumpi Song',
        artist='Spritney Bears',
    )


def create_target_directory_and_copy(source, dest):
    target_dir = os.path.dirname(dest)
    if not os.path.exists(target_dir):
        os.makekdirs(target_dir)
    shutil.copy2(source, dest)
