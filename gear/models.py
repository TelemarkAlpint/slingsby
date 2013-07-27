# coding: utf-8

from django.contrib.auth.models import User
from django.db import models

class Gear(models.Model):
    name = models.CharField('produktnavn', max_length=100)
    gear_id = models.CharField('utstyrs-ID', max_length=30)
    description = models.TextField('beskrivelse')
    img = models.URLField('bilde', null=True, blank=True)
    date_added = models.DateTimeField('dato lagt inn', auto_now_add=True)

    class Meta:
        verbose_name_plural = 'gear'

    def __json__(self):
        return dict(
                    id=self.id,
                    gear_id=self.gear_id,
                    description=self.description,
                    name=self.name,
                    image=self.img,
                    date_added=self.date_added,
                    )

    def __unicode__(self):
        return '<Gear: %s (%s)>' % (self.name, self.gear_id)

class Reservation(models.Model):
    gear = models.ForeignKey(Gear)
    start_date = models.DateTimeField('fra')
    end_date = models.DateTimeField('til')
    user = models.ForeignKey(User)
    date_added = models.DateTimeField('dato lagt inn', auto_now_add=True)
