# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_auto_20150317_1139'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='event',
            options={'ordering': ['startdate'], 'permissions': (('early_signup', 'Can signup to events before regular opening'),)},
        ),
    ]
