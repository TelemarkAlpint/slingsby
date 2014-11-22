# coding: utf-8

from __future__ import unicode_literals

from os import path
from datetime import datetime
from django import forms
from django.db import models
from django.conf import settings
from django.forms import ModelForm
from logging import getLogger
import time
import re


_logger = getLogger(__name__)


class Event(models.Model):
    name = models.CharField(max_length=100)
    startdate = models.CharField(max_length=10)
    enddate = models.CharField(max_length=10, null=True, blank=True)


    class Meta:
        ordering = ['-startdate', 'name']


    @property
    def year(self):
        return self.startdate.split('-')[0]


    def __unicode__(self):
        return '(%s) %s' % (self.startdate, self.name)


    @property
    def images(self):
        images = self._images.filter(ready=True).all()
        return images


    def to_json(self):
        return {
            'name': self.name,
            'startDate': self.startdate.isoformat(),
            'endDate': self.enddate.isoformat(),
            'images': [i.to_json() for i in self.images],
        }


def get_image_filename(instance, orig_filename):
    """ Get the temporary filename of an image while it's on the webserver.

    Will get a new name when moved to the fileserver.
    """
    extension = path.splitext(orig_filename)[1]
    filename = 'temp-archive-images/%s-original%s' % (int(time.time()*1000), extension)
    _logger.info('Saving uploaded image to %s', filename)
    return filename


class Image(models.Model):
    original = models.FileField(max_length=200, upload_to=get_image_filename)
    original_filename = models.CharField('opprinnelig filnavn', max_length=100)
    original_height = models.IntegerField('Original høyde')
    original_width = models.IntegerField('Original bredde')
    datetime_taken = models.DateTimeField('dato tatt')
    _description = models.TextField(blank=True, default='')
    event = models.ForeignKey(Event, related_name='_images')
    photographer = models.CharField('fotograf', max_length=100)
    ready = models.BooleanField(default=False)


    class Meta:
        verbose_name = 'bilde'
        verbose_name_plural = 'bilder'
        ordering = ['datetime_taken']
        permissions = (
            ('can_upload_images', 'Can upload new images to the archive'),
        )


    def __unicode__(self):
        return 'Bilde %s (%s)' % (self.id, self.original_filename)


    def get_absolute_url(self):
        return settings.MEDIA_URL + self.original


    @property
    def thumbnail(self):
        base, ext = path.splitext(self.original.url)
        base = base.rsplit('-', 1)[0]
        base += '-thumb'
        return base + ext


    @property
    def websize(self):
        base, ext = path.splitext(self.original.url)
        base = base.rsplit('-', 1)[0]
        base += '-web'
        return base + ext


    @property
    def description(self):
        descr = 'Foto av %s.' % self.photographer
        if self._description:
            descr += ' ' + self._description
        return descr


    def to_json(self):
        return {
            'websize': self.websize,
            'thumbnail': self.thumbnail,
            'original': self.original.url,
            'datetime_taken': self.datetime_taken.isoformat(),
            'description': self.description,
        }


class ImageForm(ModelForm):
    class Meta:
        model = Image
        exclude = (
            'original_filename',
            'original_height',
            'original_width',
        )


class EventForm(ModelForm):
    class Meta:
        model = Event


    def validate_datestring(self, datestring):
        """ Validates a variable precision datestring, such as "2014" or "2014-10-12". """
        datestring = datestring.strip()
        if not re.match(r'^\d{4}(-\d{2}(-\d{2})?)?$', datestring):
            raise forms.ValidationError('Feltet må være på formen <år>, <år>-<måned> eller '
                '<år>-<måned>-<dag>.')
        # Make sure there's at least three elements in the list
        parts = datestring.split('-') + [None, None]
        year, month, day = parts[:3]
        if not 1985 <= int(year) <= datetime.utcnow().year:
            raise forms.ValidationError("Ikke gyldig år, må være mellom 1985 og i år! Var %s."
                % year)
        if month and not 1 <= int(month) <= 12:
            raise forms.ValidationError('Ikke gyldig måned, må være mellom 1 og 12, var %s'
                % month)
        if day:
            try:
                datetime(int(year), int(month), int(day))
            except ValueError:
                raise forms.ValidationError('Ikke gyldig dato: %s-%s-%s' % (year, month, day))
        return datestring


    def clean_startdate(self):
        value = self.cleaned_data['startdate']
        value = self.validate_datestring(value)
        return value


    def clean_enddate(self):
        value = self.cleaned_data['enddate']
        if value:
            value = self.validate_datestring(value)
        return value
