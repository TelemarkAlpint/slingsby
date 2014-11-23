# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='datetime_taken',
            field=models.DateTimeField(default=datetime.datetime.utcnow, verbose_name='dato tatt'),
        ),
        migrations.AlterField(
            model_name='image',
            name='photographer',
            field=models.CharField(default='', max_length=100, verbose_name='fotograf', blank=True),
        ),
    ]
