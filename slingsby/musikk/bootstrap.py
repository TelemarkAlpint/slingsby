from .models import Song

def bootstrap():
    Song.objects.get_or_create(title='Danger Zone',
        artist='Kenny Loggins',
        popularity=30,
        ready=True,
    )
    Song.objects.get_or_create(title='Radioactive',
        artist='Imagine Dragons',
        ready=True,
    )
    Song.objects.get_or_create(title='Better Off Alone',
        artist='Alice Deejay',
        popularity=50,
        ready=True,
    )
