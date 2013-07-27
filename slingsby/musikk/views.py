# coding: utf-8

from ..general import make_title, reverse_with_params, feedback, cache, time
from ..general.cache import CachedQuery
from ..general.constants import MEDIA_DIR, MUSIC_DIR
from ..general.time import nor
from .models import Song, SongSuggestionForm, ReadySongForm, Vote
from .. import upload
from contextlib import closing
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models.signals import post_save
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.views.generic.simple import direct_to_template
from urllib2 import urlopen
from dateutil.parser import parse
import datetime
import json
import logging

_SONGS_IN_TOP_SONGS = 33
_EXPONENTIAL_BASE = 0.9917

class TopSongsCache(CachedQuery):
    keyword = 'top_songs'
    queryset = Song.objects.filter(ready=True).filter(votes__gt=0)[:_SONGS_IN_TOP_SONGS]

class AllReadySongsCache(CachedQuery):
    keyword = 'ready_songs'
    queryset = Song.objects.filter(ready=True).order_by('artist', 'title')

post_save.connect(AllReadySongsCache.empty_on_save, Song)

def song_details(request, song_id):
    song = get_object_or_404(Song, pk=song_id)
    if request.prefer_json:
        return HttpResponse(json.dumps(song.__json__()), mimetype='application/json')
    values = {
              'song': song,
              'title': make_title(song.title),
              }
    return direct_to_template(request, 'musikk/song_details.html', values)

def get_vote_dict(user):
    """ Find the ids of the songs the user has voted on today. """
    if not user.is_authenticated():
        return {}
    dictionary = cache.get('vote_dict')
    if dictionary is None or user.id not in dictionary.keys():
        date = time.now().date()
        start = nor.localize(datetime.datetime(date.year, date.month, date.day))
        values = Vote.objects.filter(date_added__gte=start).filter(user=user).values('song')
        ids = [d.values()[0] for d in values]
        dictionary = {user.id: ids}
        cache.set('vote_dict', dictionary)
    return dictionary

def all_songs(request):
    all_songs = AllReadySongsCache.get_cached()
    if request.prefer_json:
        json_array = [song.__json__() for song in all_songs]
        return HttpResponse(json.dumps(json_array), mimetype='application/json')
    user = request.user
    first_half, second_half = split_list_in_half(all_songs)
    vote_dict = get_vote_dict(user)
    songs_voted_on = vote_dict.get(user.id, [])
    top_songs = TopSongsCache.get_cached()
    values = {
        'songs_voted_on': songs_voted_on,
        'top_songs': top_songs,
        'all_songs_first_half': first_half,
        'all_songs_second_half': second_half,
        'song_form': SongSuggestionForm(),
        'title': make_title('Musikk'),
        'song_dir': MEDIA_DIR + 'songs/'
    }
    if user.is_staff:
        values['new_songforms'] = get_new_songforms()
    return direct_to_template(request, 'musikk/musikk.html', values)

def split_list_in_half(array):
    length = array.count()
    if length % 2 == 0:
        center = length//2
    else:
        center = length//2 + 1
    return array[:center], array[center:]

def get_new_songforms():
    songs = Song.objects.filter(ready=False).order_by('date_added')
    forms = [ReadySongForm(instance=song) for song in songs]
    return forms

def top(request):
    song_metadata = get_top_song_metadata()
    cache.set('top_song_filename', song_metadata['filename'])
    last_updated = parse(song_metadata['last_updated'])
    values = {'last_updated': last_updated.strftime("%d.%m.%y %H:%M"),
              'num_songs': _SONGS_IN_TOP_SONGS,
              }
    return direct_to_template(request, 'musikk/top.html', values)

def top_song(request):
    """ Get the location of the latest song merged from the top songs. """
    metadata = get_top_song_metadata()
    filename = metadata['filename']
    return HttpResponseRedirect(MUSIC_DIR + filename)

def get_top_song_metadata():
    """ Fetch the JSON metadata about the latest top song from the fileserver. """
    with closing(urlopen(MUSIC_DIR + 'top_meta.json')) as json_data:
        return json.load(json_data)

def top_list(request):
    top_songs = list(TopSongsCache.update_cache())
    final_list = []
    for song in top_songs:
        final_list.append(song.__json__(verbose=True))
    return HttpResponse(json.dumps(final_list, indent=2), mimetype='application/json')

@login_required
@require_POST
def upload_song(request):
    redirect = reverse_with_params('musikk', feedback.SONG_THANKS)
    self_url = reverse('musikk.views.upload_song')
    song = SongSuggestionForm(request.POST).save(commit=False)
    song.suggested_by = request.user
    song.save()
    return upload.upload(request, SongSuggestionForm, self_url, redirect,
                  custom_log="", instance=song)

@staff_member_required
@require_POST
def approve_song(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    song.ready = True
    song.save()
    func = AllReadySongsCache.empty_cache
    redirect = reverse_with_params('musikk.views.all_songs',
                                   feedback.SONG_READY.format_string(song))
    return upload.upload(request, ReadySongForm, reverse('musikk.views.approve_song'),
                  redirect, song, func, "", song)

def set_vote_dict(dictionary):
    cache.set('vote_dict', dictionary)

@login_required
@require_POST
def vote_on_song(request, song_id):
    """ Register a vote for a song, if the user can vote on it. """

    song = get_object_or_404(Song, pk=song_id)
    user = request.user
    vote_dict = get_vote_dict(user)
    can_vote = song.id not in vote_dict[user.id] and song.ready
    if can_vote:
        vote = Vote()
        vote.user = user
        vote.song = song
        vote.save()
        vote_dict[user.id].append(song.id)
        set_vote_dict(vote_dict)
        logging.info('%s voted on %s.', song)
        return HttpResponse('Vote registered on %s.' % song)
    else:
        logging.info('%s tried to vote more than once on %s.' % (user.username, song))
        return HttpResponse("Du har allerede stemt på denne sangen i dag!", content_type='text/plain', status=403)

@staff_member_required
@require_POST
def delete_song(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    song.delete()
    redirect = reverse_with_params('musikk.views.all_songs',
                                   feedback.SONG_DELETED.format_string(song))
    return HttpResponseRedirect(redirect)
