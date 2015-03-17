# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def convert_participant_ids_to_signups(apps, schema_editor):
    Event = apps.get_model('events', 'Event')
    User = apps.get_model('auth', 'User')
    Signup = apps.get_model('events', 'Signup')
    events = Event.objects.exclude(participants_by_id__exact='').exclude(participants_by_id__isnull=True)
    for event in events:
        csv_user_ids = event.participants_by_id
        user_ids = csv_user_ids.split(',')
        for user_id in user_ids:
            user = User.objects.get(id=user_id)
            Signup.objects.create(event=event, user=user)


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_auto_20150317_1159'),
    ]

    operations = [
        migrations.RunPython(
            convert_participant_ids_to_signups,
        ),
        migrations.RenameField(
            model_name='event',
            old_name='comittee_registration_opens',
            new_name='_comittee_registration_opens',
        ),
        migrations.RemoveField(
            model_name='event',
            name='participants_by_id',
        ),
    ]
