# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import slingsby.archive.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('startdate', models.CharField(max_length=10)),
                ('enddate', models.CharField(max_length=10, null=True, blank=True)),
            ],
            options={
                'ordering': ['-startdate', 'name'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('original', models.FileField(max_length=200, upload_to=slingsby.archive.models.get_image_filename)),
                ('original_filename', models.CharField(max_length=100, verbose_name='opprinnelig filnavn')),
                ('original_height', models.IntegerField(verbose_name='Original h\xf8yde')),
                ('original_width', models.IntegerField(verbose_name='Original bredde')),
                ('datetime_taken', models.DateTimeField(verbose_name='dato tatt')),
                ('_description', models.TextField(default='', blank=True)),
                ('photographer', models.CharField(max_length=100, verbose_name='fotograf')),
                ('ready', models.BooleanField(default=False)),
                ('event', models.ForeignKey(related_name='_images', to='archive.Event')),
            ],
            options={
                'ordering': ['datetime_taken'],
                'verbose_name': 'bilde',
                'verbose_name_plural': 'bilder',
                'permissions': (('can_upload_images', 'Can upload new images to the archive'),),
            },
            bases=(models.Model,),
        ),
    ]
