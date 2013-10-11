from ..general.constants import LOGOUT_URL
from django.contrib.auth import logout as django_logout
from django.contrib.auth.views import logout as social_logout
from django.http import HttpResponseRedirect
from django.views.generic.base import View
from logging import getLogger
from social_auth.backends.pipeline.social import social_auth_user

_logger = getLogger(__name__)

class LogoutView(View):

    def get(self, request):
        if social_auth_user:
            social_logout(request)
            return HttpResponseRedirect('/')
        else:
            django_logout(request)
            return HttpResponseRedirect(LOGOUT_URL)
