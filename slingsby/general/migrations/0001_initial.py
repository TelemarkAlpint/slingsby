# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Sponsor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name=b'navn')),
                ('date_added', models.DateField(auto_now_add=True)),
                ('filename', models.CharField(help_text=b'Filnavnet til logoen i media/img/sponsor-mappa.\n                                Bildet b\xc3\xb8r v\xc3\xa6re 240x40px.', max_length=100, verbose_name=b'filnavn')),
                ('webpage', models.URLField(verbose_name=b'hjemmeside')),
                ('importance', models.IntegerField(default=1, help_text=b'Brukes til \xc3\xa5 sortere sponsorene\n                                p\xc3\xa5 siden, jo h\xc3\xb8yere tall jo lenger opp kommer de.', verbose_name=b'viktighet')),
            ],
            options={
                'ordering': ['-importance'],
            },
            bases=(models.Model,),
        ),
    ]
