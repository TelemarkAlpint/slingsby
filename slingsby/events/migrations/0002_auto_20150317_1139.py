# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Signup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('signup_time', models.DateTimeField(auto_now=True, verbose_name='p\xe5meldingstid')),
                ('event', models.ForeignKey(to='events.Event')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('event', 'signup_time'),
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='event',
            name='comittee_registration_opens',
            field=models.DateTimeField(null=True, verbose_name='komit\xe9medlemp\xe5melding \xe5pner', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='reserved_spots_for_committee_members',
            field=models.IntegerField(help_text='Blank = 40%', null=True, verbose_name='Reserverte plasser for komit\xe9medlemmer', blank=True),
            preserve_default=True,
        ),
    ]
