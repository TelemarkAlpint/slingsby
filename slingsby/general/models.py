# coding: utf-8

from .cache import CachedQuery

from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.utils.http import urlquote

class Sponsor(models.Model):
    name = models.CharField('navn', max_length=100)
    date_added = models.DateField(auto_now_add=True)
    filename = models.CharField('filnavn', max_length=100,
                                help_text='''Filnavnet til logoen i media/img/sponsor-mappa.
                                Bildet bør være 240x40px.''')
    webpage = models.URLField('hjemmeside')
    importance = models.IntegerField('viktighet', default=1, help_text='''Brukes til å sortere sponsorene
                                på siden, jo høyere tall jo lenger opp kommer de.''')

    class Meta:
        ordering = ['-importance']

    def __unicode__(self):
        return self.name

    def get_img_url(self):
        return settings.MEDIA_DIR + 'img/sponsors/' + urlquote(self.filename)

class SponsorsQuery(CachedQuery):
    keyword = 'sponsors'
    queryset = Sponsor.objects.all()
post_save.connect(SponsorsQuery.empty_on_save, sender=Sponsor)
