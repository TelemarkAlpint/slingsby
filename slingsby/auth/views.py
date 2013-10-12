from django.contrib.auth.views import logout as social_logout
from django.http import HttpResponseRedirect
from django.views.generic.base import View
from logging import getLogger

_logger = getLogger(__name__)

class LogoutView(View):

    def get(self, request):
        social_logout(request)
        return HttpResponseRedirect('/')
