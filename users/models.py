from django import forms
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.forms.models import ModelForm
import logging

class UserProfile(models.Model):
    user = models.OneToOneField(User, verbose_name='bruker')
    is_member = models.BooleanField('medlem', default=False)
    full_name = models.CharField('fullt navn', max_length=140, null=True)
    ntnui_id = models.IntegerField('NTNUI ID', null=True, blank=True)
    has_image = models.BooleanField('Har bilde?', default=False)
    
    def full_name_or_username(self):
        return self.full_name or self.user.username
    username = property(full_name_or_username)
    
    def __ne__(self, other):
        return self.user != other.user
    
    def __eq__(self, other):
        return self.user == other.user  
    
    def __unicode__(self):
        return self.username
    
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        name = get_full_name(instance)
        UserProfile.objects.create(user=instance, full_name=name)
        
post_save.connect(create_user_profile, sender=User)
User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])

class AdminProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile

class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ('full_name', )

class NameLookup(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    
    def __unicode__(self):
        return '%s (%s)' % (self.name, self.email)
    
def get_full_name(user):
    lookup = NameLookup.objects.filter(email=user.email)
    if lookup:
        if len(lookup) == 1:
            full_name = lookup[0].name
            return full_name
        else:
            logging.warning('Bad name lookup: %s' % str(lookup))
    return ''