# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.forms import ModelForm, Textarea

#TODO: suggested_by bare i en overgangsfase mens gamle quotes får lagt inn feltet
class Quote(models.Model):
    topic = models.CharField('om...', max_length=100, null=True, blank=True)
    quote = models.TextField("sitat")
    author = models.CharField('hvem', max_length=100)
    date_added = models.DateTimeField('lagt inn', auto_now_add=True)
    suggested_by = models.ForeignKey(User, related_name='suggested_quotes', null=True, verbose_name='foreslått av')
    accepted = models.BooleanField('godkjent', default=False)

    class Meta:
        permissions = (
            ('approve_quote', 'Can approve a suggested quote'),
        )


    def __unicode__(self):
        if self.topic:
            return '%s om %s' % (self.author, self.topic)
        else:
            ellipses = '...' if len(self.quote) > 30 else ''
            return '%s: %s' % (self.author, self.quote[:30] + ellipses)


    def to_json(self):
        json = {
            'id': self.id,
            'quote': self.quote,
            'author': self.author,
            'date_added': self.date_added.isoformat(),
            'approved': self.accepted,
        }
        if self.topic:
            json['topic'] = 'Om %s' % self.topic
        if self.suggested_by is not None:
            json['suggested_by'] = self.suggested_by.username
        return json


    def get_absolute_url(self):
        return reverse('show_quote', kwargs={'quote_id': str(self.id)})


class QuoteForm(ModelForm):

    class Meta:
        model = Quote
        exclude = ('suggested_by', 'accepted')
        widgets = {
            'quote': Textarea(attrs={'cols': 20, 'rows': 3})
        }
