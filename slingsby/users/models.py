# -*- coding: utf-8 -*-

from . import base62
from .exceptions import AlreadyVerifiedException, TokenExpiredException

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.crypto import constant_time_compare
from django.dispatch import receiver
from django.db.models.signals import post_save
import datetime
import os

_email_expiration_time = datetime.timedelta(days=2)

class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    chosen_email = models.EmailField('valgt epost', blank=True, null=True)
    email_confirmed_at = models.DateTimeField('epost bekreftet', blank=True,
        null=True)
    email_challenge = models.CharField('epost challenge token', unique=True,
        max_length=32, blank=True, null=True)
    email_token_expiration_date = models.DateTimeField('challenge token '
        'utløpsdato', blank=True, null=True)
    member_since = models.DateTimeField('medlem siden', blank=True, null=True)


    def set_challenge_token(self):
        # 16 bytes provides 128 bits of entropy, which is plenty, but does
        # not fully utilize the final chunk when encoded as base62. 18 bytes
        # fully utilizes this last chunk, and has even greater entropy.
        random_bytes = os.urandom(18)
        self.email_token_expiration_date = timezone.now() + _email_expiration_time
        self.email_challenge = base62.encode(random_bytes)


    def confirm_email(self, confirmation_key):
        if self.email_confirmed_at:
            raise AlreadyVerifiedException()
        if timezone.now() >= self.email_token_expiration_date:
            raise TokenExpiredException()
        if constant_time_compare(self.email_challenge, confirmation_key):
            self.email_confirmed_at = timezone.now()
            self.email_challenge = None
            return True
        return False


    def set_unconfirmed_email(self, email):
        self.chosen_email = email
        self.set_challenge_token()
        self.email_confirmed_at = None



# Automatically create a profile object for new users
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
