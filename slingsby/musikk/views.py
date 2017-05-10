# coding: utf-8

from ..general import make_title, time
from ..general.views import ActionView
from .models import Song, SongSuggestionForm, ReadySongForm, Vote
from .tasks import process_new_song, count_votes


from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView, RedirectView, View
from dateutil.parser import parse
from time import time as get_timestamp
import json
import logging
import requests

_SONGS_IN_TOP_SONGS = 36
_EXPONENTIAL_BASE = 0.9917

_logger = logging.getLogger(__name__)

top_songs = Song.objects.filter(ready=True).filter(votes__gt=0)[:_SONGS_IN_TOP_SONGS] # pylint: disable=invalid-name
all_songs = Song.objects.filter(ready=True).order_by('artist', 'title') # pylint: disable=invalid-name


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
        if not request.user.has_perm('musikk.approve_song'):
            _logger.info("Rejected %s from deleting songs", request.user)
            return HttpResponseForbidden("Du har ikke tilgang til å slette sanger, beklager.")
        context = self.get_context_data(**kwargs)
        song = context['song']
        song.delete()
        messages.success(request, 'Poof, %s er nå slettet!' % song)
        _logger.info("%s successfully deleted by %s", song, request.user)
        return HttpResponseRedirect(reverse('musikk'))


    @method_decorator(permission_required('musikk.approve_song'))
    def approve(self, request, **kwargs):
        context = self.get_context_data(**kwargs)
        _logger.info("%s is approving song %s", request.user, context['song'])
        song = context['song']
        form = ReadySongForm(request.POST, request.FILES, instance=song)
        if form.is_valid():
            song.save()
            messages.success(request, '%s ble registrert, takker og bukker!' % song)
            _logger.info("%s approved by %s", song, request.user)
            process_new_song.delay(song.id)
            return HttpResponseRedirect(reverse('musikk'))
        else:
            songs = Song.objects.filter(ready=False, filename='').order_by('date_added')
            forms = []
            for _song in songs:
                if _song == song:
                    forms.append(form)
                else:
                    forms.append(ReadySongForm(instance=_song))
            messages.error(request, 'Du har noen feil i skjemaet, prøv på nytt pretty please?')
            _logger.info("%s was rejected for approval, invalid form data entered by %s. " +
                "Errors was: %s", song, request.user, repr(form.errors))
            context['new_songforms'] = forms
            context['song_form'] = SongSuggestionForm()
            return render(request, 'musikk/musikk.html', context, status=400)


    def vote(self, request, **kwargs):
        """ Register a vote for a song, if the user can vote on it. """
        context = self.get_context_data(**kwargs)
        _logger.info("%s is trying to vote on %s", request.user, context['song'])
        votes = get_votes_from_today(request.user)
        can_vote = context['song'].id not in votes and context['song'].ready
        if can_vote:
            Vote.objects.create(user=request.user, song=context['song'])
            logging.info('%s voted on %s.', request.user, context['song'])
            count_votes.delay()
            update_top_songs()
            return HttpResponse('Vote registered on %s.' % context['song'])
        else:
            logging.info('%s tried to vote more than once on %s.',
                request.user.username, context['song'])
            return HttpResponse("Du har allerede stemt på denne sangen i dag!",
                content_type='text/plain', status=403)


def update_top_songs(self):
    self.top_songs = Song.objects.filter(ready=True).filter(votes__gt=0)[:_SONGS_IN_TOP_SONGS]

def get_votes_from_today(user):
    """ Find the ids of the songs the user has voted on today. """
    if not user.is_authenticated():
        return set()
    start_of_day = time.now().replace(hour=0, minute=0, second=1)
    values = list(Vote.objects.filter(date_added__gte=start_of_day, user=user).values_list('song', flat=True))
    return set(values)


class AllSongsView(TemplateView):

    template_name = 'musikk/musikk.html'

    def get(self, request, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


    def post(self, request, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponse('Authenticate first', status=401)
        form = SongSuggestionForm(request.POST)
        context = self.get_context_data(**kwargs)
        if form.is_valid():
            song = form.save(commit=False)
            song.suggested_by = request.user
            song.save()
            _logger.info("User %d suggested song: %s", request.user.id, song)
            messages.success(request, 'Takker og bukker, webmaster vil se på forslaget og ' \
                'prøve å få lastet det opp ASAP, hang tight!')
            return HttpResponseRedirect(reverse('musikk'))
        else:
            messages.warning(request, 'Oops, ser ut til at du har noen feil i skjemaet, ' \
                'se om du får fikset det og prøv på nytt!')
            context['song_form'] = form
            return self.render_to_response(context, status=400)


    def get_context_data(self, **kwargs):
        context = super(AllSongsView, self).get_context_data(**kwargs)
        user = self.request.user
        first_half, second_half = self._split_list_in_half(all_songs.all())

        context['songs_voted_on'] = get_votes_from_today(user)
        context['top_songs'] = top_songs.all()
        context['all_songs_first_half'] = first_half
        context['all_songs_second_half'] = second_half
        context['song_form'] = SongSuggestionForm()
        context['title'] = make_title('Musikk')
        context['MEDIA_URL'] = settings.MEDIA_URL

        if user.has_perm('musikk.approve_song'):
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
        """ Get suggested songs that have not been processed yet (ie ready=False and
        no filename)
        """
        songs = Song.objects.filter(ready=False, filename='').order_by('date_added')
        forms = [ReadySongForm(instance=song) for song in songs]
        return forms


class TopSongsView(TemplateView):

    template_name = 'musikk/top.html'

    def get_context_data(self, **kwargs):
        context = super(TopSongsView, self).get_context_data(**kwargs)
        song_metadata = get_top_song_metadata()
        last_updated = parse(song_metadata['last_updated'])
        context['last_updated'] = last_updated.strftime("%d.%m.%y %H:%M")
        context['num_songs'] = _SONGS_IN_TOP_SONGS
        context['top_song_url'] = song_metadata['url']
        return context


class TopSong(RedirectView):

    permanent = False

    def get_redirect_url(self, **kwargs):
        """ Get the location of the latest song merged from the top songs. """
        metadata = get_top_song_metadata()
        song_url = metadata['url']
        return song_url


class TopSongsList(View):

    def get(self, request):
        top_songs_data = {
            'songs': [song.to_json() for song in top_sontopgs.all()],
        }
        return HttpResponse(json.dumps(top_songs_data, indent=2), content_type='application/json')


def get_top_song_metadata():
    """ Fetch the JSON metadata about the latest top song from the fileserver. """
    cache_buster = '?v=%s' % get_timestamp()
    response = requests.get(settings.MEDIA_URL + 'musikk/top_meta.json' + cache_buster)
    return response.json()
