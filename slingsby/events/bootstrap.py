# -*- coding: utf-8 -*-

from .models import Event
from ..general.time import now

from datetime import timedelta

def bootstrap():
    Event.objects.get_or_create(name='Alpetur',
        has_registration=True,
        binding_registration=True,
        number_of_spots=20,
        summary='Vi skal til Bad Gastein!',
        description='''<p>
                Lang tur ja.
            </p>''',
        location='Bad Gastein',
        defaults={
            'startdate': (now() + timedelta(hours=3)),
            'enddate': (now() + timedelta(days=6)),
            'registration_opens': (now() + timedelta(minutes=2)),
            'registration_closes': (now() + timedelta(minutes=5)),
        }
    )

    Event.objects.get_or_create(name='Skifestivalen',
        has_registration=False,
#        number_of_spots=0,
        summary='Fest med ski på beina.',
        description='''<p>
                Ski, øl og grill, hva kan bli bedre enn dette?
            </p>''',
        location='Gråkallen',
        defaults={
            'startdate': (now() + timedelta(days=30)),
            'enddate': (now() + timedelta(days=30, hours=5)),
        }
    )
