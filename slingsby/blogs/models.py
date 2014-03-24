# coding: utf-8

from ..general import time, validate_text
from ..general.time import nor_to_utc, is_past
from ..general.widgets import WidgEditorWidget, NORDateTimeWidget
from .widgets import SocialSummaryWidget
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from django.forms import ModelForm

class Blog(models.Model):
    """
    En modell for alle blogger som lastes opp i systemet.
    """
    visible = models.BooleanField('synlig', default=True)
    published_date = models.DateTimeField('publiseres', blank=True,
                                          help_text='''Kan settes inn i fremtiden hvis du vil at en artikkel skal bli
                                          synlig ved en senere anledning''')
    last_edited = models.DateTimeField('sist endret', null=True, blank=True)
    last_edited_by = models.ForeignKey(User, null=True, blank=True, related_name='User.User.blog_set')
    title = models.CharField('tittel', max_length=200, blank=False)
    content = models.TextField('innhold')
    author = models.ForeignKey(User, related_name='User.User.blog_Set', blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    social_summary = models.TextField('sosialt sammendrag', blank=True, null=True,
        help_text='Dette er teksten som vises hvis du deler artikkelen på facebook. Anbefalt maks 300 tegn.')


    class Meta:
        ordering = ['-published_date']


    def __unicode__(self):
        return self.title


    def __json__(self):
        data = {
                'id': self.id,
                'published_date': self.published_date.isoformat(),
                'title': self.title,
                'visible': self.visible,
                'content': self.content,
                'author': self.author.username,
                }
        if self.social_summary:
            data['summary'] = self.social_summary
        if self.last_edited:
            data['last_edited'] =  self.last_edited.isoformat()
            data['last_edited_by'] =  self.last_edited_by.username
        return data


    def get_absolute_url(self):
        return reverse('blog_detail', args=[str(self.id)])


    def is_visible(self):
        has_been_published = is_past(self.published_date)
        return has_been_published and self.visible


class BlogForm(ModelForm):
    class Meta:
        model = Blog
        exclude = ('last_edited', 'last_edited_by', 'author')
        widgets = {
           'content': WidgEditorWidget(),
           'published_date': NORDateTimeWidget(),
           'social_summary': SocialSummaryWidget(),
        }

    def clean_published_date(self):
        date = self.cleaned_data['published_date']
        if not date:
            date = time.now()
        return nor_to_utc(date)

    def clean_content(self):
        data = self.cleaned_data['content']
        clean_data = validate_text(data)
        return clean_data