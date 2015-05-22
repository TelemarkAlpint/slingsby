from .models import Song

from django.utils.lorem_ipsum import words
import random

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
