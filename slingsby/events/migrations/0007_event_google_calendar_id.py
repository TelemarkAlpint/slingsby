# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_auto_20150511_0114'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='google_calendar_id',
            field=models.CharField(max_length=50, null=True, verbose_name='Google Calendar ID'),
        ),
    ]
