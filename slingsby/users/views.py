from ..general.constants import JOIN_URL, EDIT_PROFILE_IMAGE
from ..general.time import now
from ..events.models import Event
from ..musikk.models import Vote, Song
from ..users.models import UserProfileForm
from django.http import HttpResponseRedirect
from django.views.generic.simple import direct_to_template

def get_events(user):
    upcoming_events = Event.objects.filter(startdate__gte=now())
    events = []
    for event in upcoming_events:
        if event.is_user_participant(user):
            events.append(event)
    return events

def get_favorite_songs(user):
    ids_voted_on = Vote.objects.filter(user=user).values_list('song', flat=True)
    top = {}
    for song_id in ids_voted_on:
        top[song_id] = top.get(song_id, 0) + 1
    top_ids = [t[0] for t in sorted(top.items(), key=lambda d: d[1], reverse=True)[:5]]
    songs = Song.objects.filter(id__in=top_ids).values('artist', 'title', 'id')
    song_dict = {}
    for song in songs:
        song_dict[song['id']] = {'artist': song['artist'], 'title': song['title'], 'votes': top[song['id']]}
    return [song_dict[s_id] for s_id in top_ids]

def get_suggested_songs(user):
    return Song.objects.filter(suggested_by=user).values('artist', 'title', 'popularity')

def edit_profile(request):
    user = request.user
    values = {'events': get_events(user),
              'name_form': UserProfileForm(instance=user),
              'top_voted_songs': get_favorite_songs(user),
              'suggested_songs': get_suggested_songs(user),
              'EDIT_PROFILE_IMAGE': EDIT_PROFILE_IMAGE,
              }
    return direct_to_template(request, 'users/profile.html', values)

def join_group(request):
    profile = request.user.profile
    profile.is_member = True
    profile.save()
    return HttpResponseRedirect(JOIN_URL)
