from django.http import HttpResponse
from musikk.models import Vote, Song
from musikk.views import _EXPONENTIAL_BASE, AllReadySongsCache
import logging

def update_ratings(request):
    """ Count up all new votes and recalculate song ratings. """

    logging.info('Starting to count new votes...')
    all_songs = list(Song.objects.all())
    votes = Vote.objects.select_related('song').filter(counted=False)
    max_rating = 0.0
    vote_array = []
    for vote in votes:
        vote_array.append(vote.song.id)
        vote.counted = True
        vote.save()
    logging.info('%d new votes found: ' + str(vote_array))
    for song in all_songs:
        for voted_song in vote_array:
            if voted_song == song.id:
                song.votes += 1
            else:
                song.votes *= _EXPONENTIAL_BASE
        if song.votes > max_rating:
            max_rating = song.votes
    for song in all_songs:
        song.popularity = song.votes * 100 / max_rating
        song.save()
    logging.info('All votes counted.')
    AllReadySongsCache.empty_cache()
    return HttpResponse()