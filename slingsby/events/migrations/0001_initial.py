# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name=b'navn')),
                ('startdate', models.DateTimeField(verbose_name=b'startdato')),
                ('enddate', models.DateTimeField(verbose_name=b'sluttdato')),
                ('has_registration', models.BooleanField(default=False, verbose_name='p\xe5melding')),
                ('registration_opens', models.DateTimeField(null=True, verbose_name='p\xe5meldingen \xe5pner', blank=True)),
                ('registration_closes', models.DateTimeField(null=True, verbose_name='p\xe5meldingen stenger', blank=True)),
                ('binding_registration', models.BooleanField(default=False, verbose_name='bindende p\xe5melding')),
                ('number_of_spots', models.IntegerField(help_text=b'0 = ubegrenset', null=True, verbose_name=b'antall plasser', blank=True)),
                ('participants_by_id', models.CommaSeparatedIntegerField(max_length=4000, null=True, verbose_name=b'deltager-IDer', blank=True)),
                ('summary', models.TextField(verbose_name=b'sammendrag')),
                ('description', models.TextField(verbose_name=b'beskrivelse')),
                ('location', models.CharField(max_length=100, verbose_name=b'sted')),
            ],
            options={
                'ordering': ['startdate'],
            },
            bases=(models.Model,),
        ),
    ]
