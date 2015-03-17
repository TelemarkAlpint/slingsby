# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_auto_20150317_1248'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='reserved_spots_for_committee_members',
        ),
    ]
