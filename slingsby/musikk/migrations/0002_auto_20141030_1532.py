# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('musikk', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='song',
            options={'ordering': ['-votes', 'artist', 'title'], 'permissions': (('approve_song', 'Can upload new songs to suggestions'),)},
        ),
    ]
