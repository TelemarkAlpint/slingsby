# coding: utf-8

from ..general import make_title, cache, time
from ..general.cache import CachedQuery, empty_on_changes_to
from ..general.constants import MEDIA_DIR, MUSIC_DIR
from ..general.time import _nor as nor_timezone
from ..general.views import ActionView
from .models import Song, SongSuggestionForm, ReadySongForm, Vote
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView, RedirectView, View
from dateutil.parser import parse
import datetime
from time import time as get_timestamp
import json
import logging
import requests

_SONGS_IN_TOP_SONGS = 33
_EXPONENTIAL_BASE = 0.9917

_logger = logging.getLogger(__name__)


class TopSongsCache(CachedQuery):
    keyword = 'top_songs'
    queryset = Song.objects.filter(ready=True).filter(votes__gt=0)[:_SONGS_IN_TOP_SONGS]


@empty_on_changes_to(Song)
class AllReadySongsCache(CachedQuery):
    keyword = 'ready_songs'
    queryset = Song.objects.filter(ready=True).order_by('artist', 'title')


class SongDetailView(ActionView, TemplateView):

    template_name = 'musikk/song_details.html'
    actions = ('vote', 'approve')

    def get_context_data(self, **kwargs):
        context = super(SongDetailView, self).get_context_data(**kwargs)
        song_id = kwargs['song_id']
        song = get_object_or_404(Song, pk=song_id)
        context['song'] = song
        context['title'] = make_title(song.title)
        return context


    def delete(self, request, **kwargs):
        _logger.info("%s is trying to delete a song", request.user)
        if not request.user.is_staff:
            _logger.info("Rejected %s from deleting songs", request.user)
            return HttpResponseForbidden("Du har ikke tilgang til å slette sanger, beklager.")
        context = self.get_context_data(**kwargs)
        song = context['song']
        song.delete()
        msg = 'Poof, %s er nå slettet!' % song
        _logger.info("%s successfully deleted by %s", song, request.user)
        return HttpResponseRedirect(reverse('musikk') + '?msg=' + msg)


    def approve(self, request, **kwargs):
        context = self.get_context_data(**kwargs)
        _logger.info("%s is approving song %s", request.user, context['song'])
        song = context['song']
        form = ReadySongForm(request.POST, instance=song)
        if form.is_valid():
            song.ready = True
            song.save()
            msg = '%s ble registrert, takker og bukker!' % song
            _logger.info("%s approved by %s", song, request.user)
            return HttpResponseRedirect(reverse('musikk') + '?msg=' + msg)
        else:
            message = 'Sorry, did not validate, try again?'
            _logger.info("%s was rejected for approval, invalid form data entered by %s", song, request.user)
            return HttpResponseRedirect(reverse('musikk') + '?msg=' + message)


    def vote(self, request, **kwargs):
        """ Register a vote for a song, if the user can vote on it. """
        context = self.get_context_data(**kwargs)
        _logger.info("%s is trying to vote on %s", request.user, context['song'])
        vote_dict = get_vote_dict(request.user)
        can_vote = context['song'].id not in vote_dict[request.user.id] and context['song'].ready
        if can_vote:
            vote = Vote()
            vote.user = request.user
            vote.song = context['song']
            vote.save()
            vote_dict[request.user.id].append(context['song'].id)
            cache.set('vote_dict', vote_dict)
            logging.info('%s voted on %s.', request.user, context['song'])
            return HttpResponse('Vote registered on %s.' % context['song'])
        else:
            logging.info('%s tried to vote more than once on %s.', request.user.username, context['song'])
            return HttpResponse("Du har allerede stemt på denne sangen i dag!", content_type='text/plain', status=403)


def get_vote_dict(user):
    """ Find the ids of the songs the user has voted on today. """
    if not user.is_authenticated():
        return {}
    dictionary = cache.get('vote_dict')
    if dictionary is None or user.id not in dictionary.keys():
        date = time.now().date()
        start = nor_timezone.localize(datetime.datetime(date.year, date.month, date.day))
        values = Vote.objects.filter(date_added__gte=start).filter(user=user).values('song')
        ids = [d.values()[0] for d in values]
        dictionary = {user.id: ids}
        cache.set('vote_dict', dictionary)
    return dictionary

class AllSongsView(TemplateView):

    template_name = 'musikk/musikk.html'

    def get(self, request, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


    def post(self, request, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponse('Authenticate first', status=401)
        form = SongSuggestionForm(request.POST)
        context = self.get_context_data(**kwargs)
        if form.is_valid():
            song = form.save(commit=False)
            song.suggested_by = request.user
            song.save()
            context['new_songforms'].append(ReadySongForm(instance=song))
            context['feedback'] = 'Takker og bukker, webmaster vil se på forslaget og ' \
                'prøve å få lastet det opp ASAP, hang tight!'
            return self.render_to_response(context, status=201)
        else:
            context['feedback'] = 'Oops, ser ut til at du har noen feil i skjemaet, ' \
                'se om du får fikset det og prøv på nytt!'
            context['song_form'] = form
            return self.render_to_response(context)


    def get_context_data(self, **kwargs):
        context = super(AllSongsView, self).get_context_data(**kwargs)
        all_songs = AllReadySongsCache.get_cached()
        user = self.request.user
        first_half, second_half = self._split_list_in_half(all_songs)
        vote_dict = get_vote_dict(user)
        songs_voted_on = vote_dict.get(user.id, [])
        top_songs = TopSongsCache.get_cached()

        context['songs_voted_on'] = songs_voted_on
        context['top_songs'] = top_songs
        context['all_songs_first_half'] = first_half
        context['all_songs_second_half'] = second_half
        context['song_form'] = SongSuggestionForm()
        context['title'] = make_title('Musikk')
        context['song_dir'] = MEDIA_DIR + 'songs/'

        if user.is_staff:
            context['new_songforms'] = self._get_new_songforms()
        return context


    def _split_list_in_half(self, array):
        length = array.count()
        if length % 2 == 0:
            center = length//2
        else:
            center = length//2 + 1
        return array[:center], array[center:]


    def _get_new_songforms(self):
        songs = Song.objects.filter(ready=False).order_by('date_added')
        forms = [ReadySongForm(instance=song) for song in songs]
        return forms


class TopSongsView(TemplateView):

    template_name = 'musikk/top.html'

    def get_context_data(self, **kwargs):
        context = super(TopSongsView, self).get_context_data(**kwargs)
        song_metadata = get_top_song_metadata()
        cache.set('top_song_filename', song_metadata['filename'])
        last_updated = parse(song_metadata['last_updated'])
        context['last_updated'] = last_updated.strftime("%d.%m.%y %H:%M")
        context['num_songs'] = _SONGS_IN_TOP_SONGS
        context['top_song_filename'] = song_metadata['filename']
        return context


class TopSong(RedirectView):

    def get_redirect_url(self, **kwargs):
        """ Get the location of the latest song merged from the top songs. """
        metadata = get_top_song_metadata()
        filename = metadata['filename']
        return MUSIC_DIR + filename


class TopSongsList(View):

    def get(self, request):
        top_song_objects = TopSongsCache.update_cache()
        top_songs_data = [song.to_json() for song in top_song_objects]
        return HttpResponse(json.dumps(top_songs_data, indent=2), mimetype='application/json')


def get_top_song_metadata():
    """ Fetch the JSON metadata about the latest top song from the fileserver. """
    cache_buster = '?v=%s' % get_timestamp()
    response = requests.get(MUSIC_DIR + 'top_meta.json' + cache_buster)
    return response.json()
