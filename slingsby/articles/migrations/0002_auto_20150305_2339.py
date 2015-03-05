# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subpagearticle',
            name='title',
            field=models.CharField(help_text=b'Hva skal undersiden hete?', unique=True, max_length=200, verbose_name=b'tittel'),
            preserve_default=True,
        ),
    ]
