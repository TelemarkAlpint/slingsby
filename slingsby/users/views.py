from ..general.time import now
from ..general.views import ActionView
from ..events.models import Event
from ..musikk.models import Vote, Song

from django.views.generic.base import TemplateView

class UserProfileView(ActionView, TemplateView):

    template_name = 'users/profile.html'

    def get_context_data(self, **kwargs):
        context = super(UserProfileView, self).get_context_data(**kwargs)
        user = self.request.user
        context['events'] = self.get_events(user)
        context['top_voted_songs'] = self.get_favorite_songs(user)
        context['suggested_songs'] = self.get_suggested_songs(user)
        return context


    def get(self, request, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


    def get_events(self, user):
        upcoming_events = Event.objects.filter(startdate__gte=now())
        events = []
        for event in upcoming_events:
            if event.is_user_participant(user):
                events.append(event)
        return events


    def get_suggested_songs(self, user):
        return Song.objects.filter(suggested_by=user).values('artist', 'title', 'popularity')


    def get_favorite_songs(self, user):
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
