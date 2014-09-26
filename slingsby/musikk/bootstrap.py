from .models import Song

from django.contrib.webdesign.lorem_ipsum import words
import random

def bootstrap():
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
    for i in range(41):
        Song.objects.get_or_create(
            artist='Artist %d' % i,
            ready=True,
            defaults={
                'popularity': random.randint(0, 100),
                'title': ' '.join(random.sample(words(40).split(), random.randint(2, 5))).title(),
            }
        )
