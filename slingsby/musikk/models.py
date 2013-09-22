# coding: utf-8

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.forms.models import ModelForm

class Song(models.Model):
    title = models.CharField('tittel', max_length=200)
    artist = models.CharField('artist', max_length=200)
    startpoint_in_s = models.IntegerField('startpunkt i sekunder', default=0)
    filename = models.CharField('filnavn', max_length=500)
    ready = models.BooleanField('godkjent', default=False)
    date_added = models.DateTimeField('lagt inn', auto_now_add=True)
    suggested_by = models.ForeignKey(User, related_name="suggested_songs", null=True,
        verbose_name='foreslått av')
    popularity = models.FloatField('popularitet', default=0.0,
        help_text='Prosentvis hvor mange poeng sammenlignet med mest populære sang')
    votes = models.FloatField('rating', default=0.0)

    class Meta:
        ordering = ['-votes', 'artist', 'title']

    def __unicode__(self):
        return '%s - %s' % (self.artist, self.title)

    def to_json(self):
        json = {
            'id': self.id,
            'title': self.title,
            'artist': self.artist,
            'date_added': self.date_added.isoformat(),
            'popularity': self.popularity,
            'filename': self.filename,
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

class AdminVoteForm(ModelForm):
    class Meta:
        model = Vote

class AdminSongForm(ModelForm):
    class Meta:
        model = Song

class SongSuggestionForm(ModelForm):
    class Meta:
        model = Song
        fields = ('artist', 'title', 'startpoint_in_s')

class ReadySongForm(ModelForm):
    class Meta:
        model = Song
        fields = ('title', 'artist', 'filename', 'startpoint_in_s')

    def clean_filename(self):
        data = self.cleaned_data['filename']
        data = data.replace('\\', '/')
        if data.endswith('.mp3') or data.endswith('.ogg'):
            return data[:-4]
        else:
            return data
