""" Enabled in dev environemnts to be able to test the site as different users.

Doesn't require passwords, and should obviously NEVER be enabled in a prod environment.

Both DEBUG=True (url routing) and adding this to AUTHENTICATION_BACKENDS needs to be in place
for this to work.
"""

from django.contrib.auth.models import User

class DevAuthBackend(object): # pragma: no cover

    def authenticate(self, username=None):
        return User.objects.get(username=username)

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
