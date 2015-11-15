# coding: utf-8

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.forms.models import ModelForm
from os import path

def get_song_filename(instance, orig_filename):
    """ Get the temporary filename of a song while it's on the webserver.

    Will get a new name when moved to the filserver."""
    extension = path.splitext(orig_filename)[1]
    filename = path.join('local', 'musikk', '%s-raw%s' % (instance.id, extension))
    return filename


class Song(models.Model):
    title = models.CharField('tittel', max_length=200)
    artist = models.CharField('artist', max_length=200)
    startpoint_in_s = models.IntegerField('startpunkt i sekunder', default=0, blank=True)
    filename = models.FileField('fil', upload_to=get_song_filename, help_text='FLAC er foretrukket')
    ready = models.BooleanField('synlig', default=False)
    date_added = models.DateTimeField('lagt inn', auto_now_add=True)
    suggested_by = models.ForeignKey(User, related_name="suggested_songs", null=True,
        verbose_name='foreslått av')
    popularity = models.FloatField('popularitet', default=0.0,
        help_text='Prosentvis hvor mange poeng sammenlignet med mest populære sang')
    votes = models.FloatField('rating', default=0.0)

    class Meta:
        ordering = ['-votes', 'artist', 'title']
        permissions = (
            ('approve_song', 'Can upload new songs to suggestions'),
        )


    def __unicode__(self):
        return '%s - %s' % (self.artist, self.title)


    def to_json(self):
        json = {
            'id': self.id,
            'title': self.title,
            'artist': self.artist,
            'date_added': self.date_added.isoformat(),
            'popularity': self.popularity,
            'filename': self.filename.url,
        }
        return json


    def get_absolute_url(self):
        return reverse('song_details', kwargs={'song_id': str(self.id)})


class Vote(models.Model):
    date_added = models.DateTimeField('dato lagt inn', auto_now_add=True)
    song = models.ForeignKey(Song, related_name='votes_on_song', verbose_name='sang')
    user = models.ForeignKey(User, related_name='votes_by_user', verbose_name='bruker')
    counted = models.BooleanField('talt opp', default=False)

    class Meta:
        ordering = ['-date_added']

    def __unicode__(self):
        username = self.user.username
        date = self.date_added.strftime('%H:%M %d.%m.%y')
        return '(%s) %s: %s' % (date, username, self.song)


class TopSongMeta(models.Model):
    url = models.URLField('url')
    date_modified = models.DateTimeField(auto_now_add=True)


class AdminVoteForm(ModelForm):
    class Meta:
        model = Vote
        exclude = []


class AdminSongForm(ModelForm):
    class Meta:
        model = Song
        exclude = []


class SongSuggestionForm(ModelForm):
    class Meta:
        model = Song
        fields = ('artist', 'title', 'startpoint_in_s')


class ReadySongForm(ModelForm):
    class Meta:
        model = Song
        fields = ('title', 'artist', 'filename', 'startpoint_in_s')
