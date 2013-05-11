# coding: utf-8

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.forms import ModelForm, Textarea

#TODO: suggested_by, verified_by null=True bare i en overgangsfase mens gamle quotes får lagt inn feltet
#TODO: Spell correction changes suggested_by
class Quote(models.Model):
    topic = models.CharField('om...', max_length=100, null=True, blank=True)
    quote = models.TextField("sitat")
    author = models.CharField('opphavsmann', max_length=100)
    date_added = models.DateTimeField('lagt inn', auto_now_add=True)
    suggested_by = models.ForeignKey(User, related_name='suggested_quotes', null=True, verbose_name='foreslått av')
    accepted = models.BooleanField('godkjent', default=False)

    def __unicode__(self):
        if self.topic:
            return '%s om %s' % (self.author, self.topic)
        else:
            ellipses = '...' if len(self.quote) > 30 else ''
            return '%s: %s' % (self.author, self.quote[:30] + ellipses)

    def __json__(self, verbose=False):
        fields = {
                  'id': self.id,
                  'quote': self.quote,
                  'author': self.author,
                  'date_added': self.date_added.isoformat(),
                  }
        if self.topic:
            fields['topic'] = 'Om %s' % self.topic
        if verbose:
            fields['approved'] = self.accepted
            if self.suggested_by is not None:
                fields['suggested_by'] = self.suggested_by.username
        return fields

    def get_absolute_url(self):
        return reverse('quotes.views.show_quote', args=[str(self.id)])

class QuoteForm(ModelForm):
    class Meta:
        model = Quote
        exclude = ('suggested_by', 'accepted')
        widgets = {
            'quote': Textarea(attrs={'cols': 20, 'rows': 5})
        }