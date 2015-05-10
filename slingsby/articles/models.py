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

class Article(models.Model):
    """
    En modell for alle artikler som lastes opp i systemet.
    """
    visible = models.BooleanField('synlig', default=True)
    published_date = models.DateTimeField('publiseres', blank=True,
                                          help_text='''Kan settes inn i fremtiden hvis du vil at en artikkel skal bli
                                          synlig ved en senere anledning''')
    last_edited = models.DateTimeField('sist endret', null=True, blank=True)
    last_edited_by = models.ForeignKey(User, null=True, blank=True, related_name='+')
    title = models.CharField('tittel', max_length=200, blank=False)
    content = models.TextField('innhold')
    author = models.ForeignKey(User, related_name='articles_written', blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    social_summary = models.TextField('sosialt sammendrag', blank=True, null=True,
        help_text='Dette er teksten som vises hvis du deler artikkelen på facebook. Anbefalt maks 300 tegn.')


    class Meta:
        verbose_name = 'artikkel'
        verbose_name_plural = 'artikler'
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
            data['last_edited'] = self.last_edited.isoformat()
            data['last_edited_by'] = self.last_edited_by.username
        return data


    def get_absolute_url(self):
        return reverse('article_detail', args=[str(self.id)])


    def is_visible(self):
        has_been_published = is_past(self.published_date)
        return has_been_published and self.visible


class ArticleForm(ModelForm):
    class Meta:
        model = Article
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

#This class is a copy-paste of Article, with some extra fields in the top. They should have both inherited from a parent
#base class, but sadly multi-table inheritance is not supported on GAE.
class SubPageArticle(models.Model):
    title = models.CharField('tittel', unique=True, blank=False, max_length=200, help_text='Hva skal undersiden hete?')
    slug = models.CharField('slug', unique=True, max_length=15, help_text="URLen siden får.")
    sort_key = models.IntegerField('sorteringsnøkkel', default=0, help_text='Jo høyere tall, jo høyere kommer siden')

    #Similar to Article from here and down
    visible = models.BooleanField('synlig', default=True)
    published_date = models.DateTimeField('publiseres', blank=True, null=True,
                                          help_text='''Kan settes inn i fremtiden hvis du vil at en artikkel skal bli
                                          synlig ved en senere anledning''')
    last_edited = models.DateTimeField('sist endret', null=True, blank=True)
    last_edited_by = models.ForeignKey(User, null=True, blank=True, related_name='+')
    content = models.TextField('innhold')
    author = models.ForeignKey(User, related_name='subpages_written', blank=True)
    date_added = models.DateTimeField(auto_now_add=True, null=True)
    social_summary = models.TextField('sosialt sammendrag', blank=True, null=True,
        help_text='Dette er teksten som vises hvis du deler artikkelen på facebook. Anbefalt maks 300 tegn.')


    class Meta:
        verbose_name = 'underside'
        verbose_name_plural = 'undersider'
        ordering = ['-sort_key', 'title']


    def __unicode__(self):
        return "Underside: /%s -> %s" % (self.slug, self.title)


    def __json__(self):
        data = {
                'id': self.id,
                'published_date': self.published_date.isoformat(),
                'title': self.title,
                'content': self.content,
                'author': self.author.username,
                'slug': self.slug,
                }
        if self.social_summary:
            data['summary'] = self.social_summary
        if self.last_edited:
            data['last_edited'] = self.last_edited.isoformat()
            data['last_edited_by'] = self.last_edited_by.username
        return data


    def get_absolute_url(self):
        return reverse('article_detail', args=[str(self.id)])


    def is_visible(self):
        has_been_published = is_past(self.published_date)
        return has_been_published and self.visible


class SubPageArticleForm(ModelForm):

    class Meta:
        model = SubPageArticle
        exclude = ('author', 'last_edited', 'last_edited_by')
        widgets = {
           'content': WidgEditorWidget(),
           'introduction': WidgEditorWidget(),
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


@receiver(post_save, sender=SubPageArticle)
def register_new_url(sender, **kwargs):
    """ Register a new valid URL when a SubPageArticle is saved. """
    # A pylint bug makes it think that urlpatterns is unused because of the +=
    # pylint: disable=unused-variable
    from .urls import urlpatterns
    from .views import ArticleDetail
    from django.conf.urls import patterns, url
    subpage = kwargs['instance']
    urlpatterns += patterns('',
        url(r'^%s$' % subpage.slug, ArticleDetail.as_view(), {'article_id': subpage.id}),
    )
