# -*- coding: utf-8 -*-

from .exceptions import AlreadyVerifiedException, TokenExpiredException
from ..general.time import now
from ..general.views import ActionView
from ..general.mail import send_templated_mail
from ..events.models import Event
from ..musikk.models import Vote, Song

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.views import logout as social_logout
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from django.views.generic.base import View, TemplateView
from logging import getLogger
from validate_email import validate_email

_logger = getLogger(__name__)

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
        # This uses GET instead of POST since the link sent in the email
        # should be clickable, which always results in a GET
        context = self.get_context_data(**kwargs)
        email_token = request.GET.get('token')
        if email_token:
            try:
                if request.user.profile.confirm_email(email_token):
                    _logger.info('User %d confirmed email %s', request.user.id,
                        request.user.profile.chosen_email)
                    messages.success(request, 'Eposten din ble bekreftet, takk.')
                    request.user.profile.member_since = timezone.now()
                    request.user.profile.save()
                else:
                    messages.error(request, 'Ikke riktig kode, prøv på nytt.')
                    _logger.info('Invalid response to challenge token for user %d',
                        request.user.id)
                    return self.render_to_response(context, status=400)
            except AlreadyVerifiedException:
                messages.warning(request, 'Du har allerede bekreftet denne epost-adressen.')
                _logger.info('User %d tried to verify an already confirmed email',
                    request.user.id)
            except TokenExpiredException:
                messages.warning(request, 'Denne koden har utløpt, klikk på knappen ved '
                    'siden av eposten din for å sende en ny.')
                _logger.info('User %d tried to confirm an email using an expired token',
                    request.user.id)
            return HttpResponseRedirect(reverse('profile'))
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


class LogoutView(View):

    def get(self, request):
        if request.user.is_authenticated():
            _logger.info('User #%d logged out', request.user.id)
            social_logout(request)
            messages.success(request, 'Du er nå logget ut, ha en fortsatt fin dag!')
        return HttpResponseRedirect('/')


class JoinView(TemplateView):

    template_name = 'users/signup.html'

    def post(self, request, **kwargs):
        chosen_email = request.POST.get('email')
        valid_email = validate_email(chosen_email)
        if not valid_email:
            messages.warning(request, 'Eposten du oppgav ser ikke ut til å '
                'være en gyldig epostadresse, prøv på nytt')
            return self.render_to_response(request, status=400)
        _logger.info('Sending email confirmation to %s', chosen_email)
        profile = request.user.profile
        profile.set_unconfirmed_email(chosen_email)
        profile.save()
        messages.success(request, 'Takk, sjekk eposten din for en mail fra oss, følg '
            'instruksjonene der for å fullføre innmeldingen. Om du ikke har '
            'fått mailen, sjekk spam-filteret ditt eller legg til '
            'noreply@ntnuita.no i kontaktlisten din og be om en ny mail.')
        send_templated_mail(subject='Bekreft eposten din for telemarkgruppa',
            template='users/mail/signup', recipient_list=[chosen_email],
            context={
            'name': request.user.get_full_name(),
            'token': profile.email_challenge,
        })
        return HttpResponseRedirect(reverse('profile'))


    def get(self, request):
        if request.user.profile.member_since:
            return HttpResponseRedirect(reverse('profile'))
        return self.render_to_response(request)


class DevLogin(TemplateView): # pragma: no cover

    template_name = 'users/devlogin.html'

    def get_context_data(self, **kwargs):
        users = User.objects.all()
        return {'users': users}


    def post(self, request):
        username = request.POST.get('username')
        if not username:
            return HttpResponse(status=400)
        user = authenticate(username=username)
        login(request, user)
        return HttpResponseRedirect('/')
