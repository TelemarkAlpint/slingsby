# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Quote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('topic', models.CharField(max_length=100, null=True, verbose_name=b'om...', blank=True)),
                ('quote', models.TextField(verbose_name=b'sitat')),
                ('author', models.CharField(max_length=100, verbose_name=b'hvem')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name=b'lagt inn')),
                ('accepted', models.BooleanField(default=False, verbose_name=b'godkjent')),
                ('suggested_by', models.ForeignKey(related_name=b'suggested_quotes', verbose_name=b'foresl\xc3\xa5tt av', to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
