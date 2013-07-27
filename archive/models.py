# coding: utf-8

from django.db import models
from general.constants import ARCHIVE_BASE_PATH

class ArchiveEvent(models.Model):
    path_hash = models.CharField(primary_key=True, max_length=40)
    date = models.CharField(max_length=16)
    enddate = models.CharField(null=True, max_length=16)
    name = models.CharField(max_length=100)

    @property
    def galleries(self):
        galleries = self._galleries.all()
        return galleries

    def __unicode__(self):
        return '(%s) %s' % (self.date, self.name)

    @property
    def videos(self):
        videos = self._videos.all()
        return videos

    class Meta:
        ordering = ['-date', 'name']

class ImageGallery(models.Model):
    path_hash = models.CharField(primary_key=True, max_length=40)
    photographer = models.CharField('fotograf', max_length=50, null=True)
    event = models.ForeignKey(ArchiveEvent, related_name='_galleries')
    cover_photo = models.CharField(max_length=200)

    @property
    def images(self):
        images = self._images.all()
        return images

    def __unicode__(self):
        name =  'Gallery <%s> ' % self.event.name
        if self.photographer:
            name += ' (%s)' % self.photographer
        return name

    class Meta:
        verbose_name_plural = 'galleries'

class Image(models.Model):
    path_hash = models.CharField(primary_key=True, max_length=40)
    medium_size_url = models.CharField(max_length=200)
    large_size_url = models.CharField(max_length=200)
    description = models.CharField(max_length=250, null=True)
    gallery = models.ForeignKey(ImageGallery, related_name='_images')

    def get_absolute_url(self):
        return ARCHIVE_BASE_PATH + self.medium_size_url

class Video(models.Model):
    video_url = models.CharField(max_length=200)
    description = models.CharField(max_length=250, null=True)
    event = models.ForeignKey(ArchiveEvent, related_name='_videos')
    path_hash = models.CharField(max_length=40)

    def get_absolute_url(self):
        return self.video_url

