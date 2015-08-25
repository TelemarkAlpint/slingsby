# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_add_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='chosen_email',
            field=models.EmailField(max_length=254, null=True, verbose_name=b'valgt epost', blank=True),
        ),
    ]
