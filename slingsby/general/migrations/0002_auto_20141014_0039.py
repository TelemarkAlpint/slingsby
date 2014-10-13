# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sponsor',
            name='filename',
        ),
        migrations.AddField(
            model_name='sponsor',
            name='image',
            field=models.CharField(default=b'', help_text=b'URL til bilde. Bildet b\xc3\xb8r v\xc3\xa6re 240x40px.', max_length=255, verbose_name=b'bilde'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sponsor',
            name='importance',
            field=models.IntegerField(default=1, help_text=b'Brukes til \xc3\xa5 sortere sponsorene p\xc3\xa5 siden, jo h\xc3\xb8yere tall jo lenger opp kommer de', verbose_name=b'viktighet'),
        ),
    ]
