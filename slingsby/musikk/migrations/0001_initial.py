# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import slingsby.musikk.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200, verbose_name=b'tittel')),
                ('artist', models.CharField(max_length=200, verbose_name=b'artist')),
                ('startpoint_in_s', models.IntegerField(default=0, verbose_name=b'startpunkt i sekunder', blank=True)),
                ('filename', models.FileField(help_text=b'FLAC er foretrukket', upload_to=slingsby.musikk.models.get_song_filename, verbose_name=b'fil')),
                ('ready', models.BooleanField(default=False, verbose_name=b'synlig')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name=b'lagt inn')),
                ('popularity', models.FloatField(default=0.0, help_text=b'Prosentvis hvor mange poeng sammenlignet med mest popul\xc3\xa6re sang', verbose_name=b'popularitet')),
                ('votes', models.FloatField(default=0.0, verbose_name=b'rating')),
                ('suggested_by', models.ForeignKey(related_name=b'suggested_songs', verbose_name=b'foresl\xc3\xa5tt av', to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['-votes', 'artist', 'title'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name=b'dato lagt inn')),
                ('counted', models.BooleanField(default=False, verbose_name=b'talt opp')),
                ('song', models.ForeignKey(related_name=b'votes_on_song', verbose_name=b'sang', to='musikk.Song')),
                ('user', models.ForeignKey(related_name=b'votes_by_user', verbose_name=b'bruker', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-date_added'],
            },
            bases=(models.Model,),
        ),
    ]
