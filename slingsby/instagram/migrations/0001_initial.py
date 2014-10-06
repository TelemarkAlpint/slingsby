# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='InstagramComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('poster', models.CharField(max_length=40, verbose_name=b'poster')),
                ('poster_image', models.URLField(verbose_name=b'posters profilbilde')),
                ('created_time', models.DateTimeField(verbose_name=b'tid opprettet')),
                ('instagram_id', models.CharField(unique=True, max_length=100, verbose_name=b'instagram id')),
                ('text', models.TextField(verbose_name=b'tekst')),
                ('visible', models.BooleanField(default=True, help_text=b'Huk vekk her hvis noen vil ha kommentaren fjernet, hvis den slettes s\xc3\xa5 vil den bare dukke opp igjen', verbose_name=b'synlig')),
            ],
            options={
                'ordering': ['created_time'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InstagramMedia',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('media_type', models.CharField(max_length=15, verbose_name=b'type')),
                ('poster', models.CharField(max_length=40, verbose_name=b'poster')),
                ('poster_image', models.URLField(verbose_name=b'posters profilbilde')),
                ('thumbnail_url', models.URLField(verbose_name=b'link til thumbnail')),
                ('media_url', models.URLField(verbose_name=b'link til media')),
                ('like_count', models.IntegerField(default=0, verbose_name=b'antall likes')),
                ('visible', models.BooleanField(default=True, help_text=b'Huk vekk her hvis noen vil ha et bilde fjernet, hvis det slettes s\xc3\xa5 vil det bare dukke opp igjen', verbose_name=b'synlig')),
                ('caption', models.TextField(verbose_name=b'tekst')),
                ('created_time', models.DateTimeField(verbose_name=b'tid opprettet')),
                ('instagram_id', models.CharField(unique=True, max_length=100, verbose_name=b'instgram id')),
            ],
            options={
                'ordering': ['-created_time'],
                'verbose_name_plural': 'instagram media',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='instagramcomment',
            name='media',
            field=models.ForeignKey(related_name=b'_comments', to='instagram.InstagramMedia'),
            preserve_default=True,
        ),
    ]
