# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('musikk', '0002_auto_20141030_1532'),
    ]

    operations = [
        migrations.CreateModel(
            name='TopSongMeta',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.URLField(verbose_name=b'url')),
                ('date_modified', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
