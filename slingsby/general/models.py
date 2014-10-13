# coding: utf-8

from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.utils.http import urlquote

class Sponsor(models.Model):
    name = models.CharField('navn', max_length=100)
    date_added = models.DateField(auto_now_add=True)
    image = models.CharField('bilde', max_length=255, default='',
                                help_text='''URL til bilde. Bildet bør være 240x40px.''')
    webpage = models.URLField('hjemmeside')
    importance = models.IntegerField('viktighet', default=1, help_text=('Brukes til å sortere '
        'sponsorene på siden, jo høyere tall jo lenger opp kommer de'))

    class Meta:
        ordering = ['-importance']

    def __unicode__(self):
        return self.name
