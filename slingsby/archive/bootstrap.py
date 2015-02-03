# pylint: disable=unpacking-non-sequence,too-many-locals

from .models import Event, Image
from ..general.utils import disconnect_signal

from django.core.files import File
from django.db.models.signals import post_save
import datetime
import os
import random

def bootstrap():
    for event in ('Romsdalssamling', 'Alpetur'):
        startdate = datetime.date(
            year=random.choice(range(1986, 2016)),
            month=random.choice(range(1, 13)),
            day=random.choice(range(1, 29)),
        )
        event, created = Event.objects.get_or_create(
            name=event,
            defaults={
                'startdate': '-'.join(startdate.strftime('%Y-%m-%d').split('-')[:random.randint(1, 3)]),
            },
        )
        if created:
            photographers = ('Even', 'Steven', 'Ine', 'Trine')
            num_images = random.randint(2, 5)
            for _ in range(num_images):
                img_number = random.randint(1, 4)
                img_path = os.path.join(os.path.dirname(__file__), 'test-data', '%d.jpg' % img_number)
                with open(img_path, 'rb') as img_fh:
                    img_file = File(img_fh)
                    with disconnect_signal(post_save, sender=Image):
                        Image.objects.get_or_create(
                            original=img_file,
                            event=event,
                            photographer=random.choice(photographers),
                            ready=True,
                        )
