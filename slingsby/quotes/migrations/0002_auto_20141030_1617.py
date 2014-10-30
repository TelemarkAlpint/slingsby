# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='quote',
            options={'permissions': (('approve_quote', 'Can approve a suggested quote'),)},
        ),
    ]
