# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


def add_missing_profiles(apps, schema_editor):
    UserProfile = apps.get_model('users', 'UserProfile')
    User = apps.get_model('auth', 'User')
    for user in User.objects.all():
        profile = UserProfile.objects.create(user=user)


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('chosen_email', models.EmailField(max_length=254, verbose_name=b'valgt epost')),
                ('email_confirmed_at', models.DateTimeField(null=True, verbose_name=b'epost bekreftet', blank=True)),
                ('email_challenge', models.CharField(max_length=32, unique=True, null=True, verbose_name=b'epost challenge token', blank=True)),
                ('email_token_expiration_date', models.DateTimeField(null=True, verbose_name=b'challenge token utl\xc3\xb8psdato', blank=True)),
                ('user', models.OneToOneField(related_name='profile', to=settings.AUTH_USER_MODEL)),
                ('member_since', models.DateTimeField(null=True, verbose_name=b'medlem siden', blank=True)),
            ],
        ),
        migrations.RunPython(
            add_missing_profiles,
        ),
    ]
