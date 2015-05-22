# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_remove_event_reserved_spots_for_committee_members'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='_comittee_registration_opens',
            field=models.DateTimeField(help_text='N\xe5r p\xe5meldingen skal \xe5pne for komit\xe9medlemmer. La v\xe6re blank for 24 timer f\xf8r vanlig \xe5pning.', null=True, verbose_name='komit\xe9medlemp\xe5melding \xe5pner', blank=True),
        ),
    ]
