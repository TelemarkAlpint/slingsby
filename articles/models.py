# coding: utf-8

from articles.widgets import SocialSummaryWidget
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from django.forms import ModelForm
from django.utils.safestring import SafeUnicode
from django.views.generic.detail import DetailView
from general import time, validate_text, make_title
from general.time import utc_to_nor, nor_to_utc, is_past
from general.widgets import WidgEditorWidget, NORDateTimeWidget
import logging

class Article(models.Model):
    """
    En modell for alle artikler som lastes opp i systemet.
    """
    visible = models.BooleanField('synlig', default=True)
    published_date = models.DateTimeField('publiseres', blank=True,
                                          help_text='''Kan settes inn i fremtiden hvis du vil at en artikkel skal bli
                                          synlig ved en senere anledning''')
    last_edited = models.DateTimeField('sist endret', null=True, blank=True)
    last_edited_by = models.ForeignKey(User, null=True, blank=True, related_name='User.User.article_set')
    title = models.CharField('tittel', max_length=200, blank=False)
    content = models.TextField('innhold')
    author = models.ForeignKey(User, related_name='User.User.article_Set', blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    social_summary = models.TextField('sosialt sammendrag', blank=True, null=True, help_text='Dette er teksten som vises hvis du deler artikkelen på facebook. Anbefalt maks 300 tegn.')

    class Meta:
        ordering = ['-published_date']

    def __unicode__(self):
        return self.title

    def __json__(self):
        data = {
                'id': self.id,
                'published_date': self.published_date.isoformat(),
                'published_date_as_string': self.get_dateline(),
                'title': self.title,
                'content': self.content,
                'author': self.author.username,
                }
        if self.social_summary:
            data['summary'] = self.social_summary
        if self.last_edited:
            data['last_edited'] =  self.last_edited.isoformat()
            data['last_edited_by'] =  self.last_edited_by.username
            data['last_edited_as_string'] = self.get_editline()
        return data

    def get_absolute_url(self):
        return reverse('article_detail', args=[str(self.id)])

    def _format_date_as_string(self, date):
        days_passed = time.days_since(date)
        if days_passed == 0:
            string = u', i dag'
        elif days_passed == 1:
            string = u', i går'
        elif days_passed == 2:
            string = u' for to dager siden'
        else:
            string = u' den %s' % date.strftime('%d.%m.%y')
        string += u', kl %s' % date.strftime('%H:%M')
        return string

    def get_dateline(self):
        logging.debug("Fetching dateline...")
        dateline = "oops"
        try:
            nor_date = utc_to_nor(self.published_date)
            datestring = self._format_date_as_string(nor_date)
            logging.info("Got so far: %s%s", self.author.username, datestring)
            dateline = 'Skrevet av %s%s.' % (self.author.username, datestring)
        except Exception as e:
            logging.warning("Failed. %s", self.author)
            logging.warning("Username: %s", self.author.username)
            logging.warning("Utc_to_nor: %s", utc_to_nor(self.published_date))
            logging.warning("formatted: %s", self._format_date_as_string(self.published_date))
            logging.warning("NOR formatted: %s", self._format_date_as_string(utc_to_nor(self.published_date)))
            logging.warning(e.message)
            import traceback
            s = traceback.format_exc()
            logging.warning(s)
#            logging.exception()
        return SafeUnicode(dateline)

    def get_editline(self):
        editline = None
        if self.last_edited:
            editline = SafeUnicode('Sist endret av %s%s.' % (
                                    self.last_edited_by.username,
                                    self._format_date_as_string(utc_to_nor(self.last_edited))))
        return editline

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
    title = models.CharField('tittel', unique=True, blank=False, max_length=30, help_text='Hva skal undersiden hete?')
    slug = models.CharField('slug', unique=True, max_length=15, help_text="URLen siden får.")
    sort_key = models.IntegerField('sorteringsnøkkel', default=0, help_text='Jo høyere tall, jo høyere kommer siden')

    #Similar to Article from here and down
    visible = models.BooleanField('synlig', default=True)
    published_date = models.DateTimeField('publiseres', blank=True, null=True,
                                          help_text='''Kan settes inn i fremtiden hvis du vil at en artikkel skal bli
                                          synlig ved en senere anledning''')
    last_edited = models.DateTimeField('sist endret', null=True, blank=True)
    last_edited_by = models.ForeignKey(User, null=True, blank=True, related_name='User.article_set')
    content = models.TextField('innhold')
    author = models.ForeignKey(User, related_name='User.article_Set', blank=True)
    date_added = models.DateTimeField(auto_now_add=True, null=True)
    social_summary = models.TextField('sosialt sammendrag', blank=True, null=True, help_text='Dette er teksten som vises hvis du deler artikkelen på facebook. Anbefalt maks 300 tegn.')

    class Meta:
        ordering = ['-sort_key', 'title']

    def __unicode__(self):
        return "<SubPageArticle: %s -> %s>" % (self.slug, self.title)

    def __json__(self):
        data = {
                'id': self.id,
                'published_date': self.published_date.isoformat(),
                'published_date_as_string': self.get_dateline(),
                'title': self.title,
                'content': self.content,
                'author': self.author.username,
                'slug': self.slug,
                }
        if self.social_summary:
            data['summary'] = self.social_summary
        if self.last_edited:
            data['last_edited'] =  self.last_edited.isoformat()
            data['last_edited_by'] =  self.last_edited_by.username
            data['last_edited_as_string'] = self.get_editline()
        return data

    def get_absolute_url(self):
        return reverse('article_detail', args=[str(self.id)])

    def _format_date_as_string(self, date):
        date = utc_to_nor(date)
        days_passed = time.days_since(date)
        if days_passed == 0:
            string = ', i dag'
        elif days_passed == 1:
            string = ', i går'
        elif days_passed == 2:
            string = ' for to dager siden'
        else:
            string = ' den %s' % date.strftime('%d.%m.%y')
        string += ', kl %s' % date.strftime('%H:%M')
        return string

    def get_dateline(self):
        dateline = 'Skrevet av %s%s.' % (self.author.username, self._format_date_as_string(utc_to_nor(self.published_date)))
        return SafeUnicode(dateline)

    def get_editline(self):
        editline = None
        if self.last_edited:
            editline = SafeUnicode('Sist endret av %s%s.' % (
                                    self.last_edited_by.username,
                                    self._format_date_as_string(utc_to_nor(self.last_edited))))
        return editline

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

class ArticleDetailView(DetailView):
    model = Article

    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        article = super(ArticleDetailView, self).get_object()
        context['title'] = make_title(article.title)
        return context

@receiver(post_save, sender=SubPageArticle)
def register_new_url(sender, **kwargs):
    """ Register a new valid URL when a SubPageArticle is saved. """
    from urls import urlpatterns
    from django.conf.urls.defaults import patterns, url
    subpage = kwargs['instance']
    urlpatterns += patterns('',
        url(r'^%s$' % subpage.slug, 'articles.views.show_article', {'article_id': subpage.id}),
                           )