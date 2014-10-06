# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('visible', models.BooleanField(default=True, verbose_name=b'synlig')),
                ('published_date', models.DateTimeField(help_text=b'Kan settes inn i fremtiden hvis du vil at en artikkel skal bli\n                                          synlig ved en senere anledning', verbose_name=b'publiseres', blank=True)),
                ('last_edited', models.DateTimeField(null=True, verbose_name=b'sist endret', blank=True)),
                ('title', models.CharField(max_length=200, verbose_name=b'tittel')),
                ('content', models.TextField(verbose_name=b'innhold')),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('social_summary', models.TextField(help_text=b'Dette er teksten som vises hvis du deler artikkelen p\xc3\xa5 facebook. Anbefalt maks 300 tegn.', null=True, verbose_name=b'sosialt sammendrag', blank=True)),
                ('author', models.ForeignKey(related_name=b'User.User.article_Set', blank=True, to=settings.AUTH_USER_MODEL)),
                ('last_edited_by', models.ForeignKey(related_name=b'User.User.article_set', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['-published_date'],
                'verbose_name': 'artikkel',
                'verbose_name_plural': 'artikler',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SubPageArticle',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(help_text=b'Hva skal undersiden hete?', unique=True, max_length=30, verbose_name=b'tittel')),
                ('slug', models.CharField(help_text=b'URLen siden f\xc3\xa5r.', unique=True, max_length=15, verbose_name=b'slug')),
                ('sort_key', models.IntegerField(default=0, help_text=b'Jo h\xc3\xb8yere tall, jo h\xc3\xb8yere kommer siden', verbose_name=b'sorteringsn\xc3\xb8kkel')),
                ('visible', models.BooleanField(default=True, verbose_name=b'synlig')),
                ('published_date', models.DateTimeField(help_text=b'Kan settes inn i fremtiden hvis du vil at en artikkel skal bli\n                                          synlig ved en senere anledning', null=True, verbose_name=b'publiseres', blank=True)),
                ('last_edited', models.DateTimeField(null=True, verbose_name=b'sist endret', blank=True)),
                ('content', models.TextField(verbose_name=b'innhold')),
                ('date_added', models.DateTimeField(auto_now_add=True, null=True)),
                ('social_summary', models.TextField(help_text=b'Dette er teksten som vises hvis du deler artikkelen p\xc3\xa5 facebook. Anbefalt maks 300 tegn.', null=True, verbose_name=b'sosialt sammendrag', blank=True)),
                ('author', models.ForeignKey(related_name=b'User.article_Set', blank=True, to=settings.AUTH_USER_MODEL)),
                ('last_edited_by', models.ForeignKey(related_name=b'User.article_set', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['-sort_key', 'title'],
                'verbose_name': 'underside',
                'verbose_name_plural': 'undersider',
            },
            bases=(models.Model,),
        ),
    ]
