# pylint: disable=unpacking-non-sequence,too-many-locals

from .models import Event, Image
from .views import get_image_capture_time

from django.core.files import File
from django.core.files.images import get_image_dimensions
import datetime
import os
import random
import shutil

def bootstrap():
    for event in ('Romsdalssamling', 'Alpetur', 'Skifestivalen', 'Pray for Snow'):
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
            num_images = random.randint(3, 15)
            for _ in range(num_images):
                img_number = random.randint(1, 4)
                img_path = os.path.join(os.path.dirname(__file__), 'test-data', '%d.jpg' % img_number)
                with open(img_path, 'rb') as img_fh:
                    img_file = File(img_fh)
                    width, height = get_image_dimensions(img_file)
                    image, _ = Image.objects.get_or_create(
                        original=img_file,
                        original_height=height,
                        original_width=width,
                        datetime_taken=get_image_capture_time(img_path),
                        event=event,
                        photographer=random.choice(photographers),
                        ready=True,
                    )
                shutil.copy2(
                    os.path.join(os.path.dirname(__file__), 'test-data', '%s-web.jpg' % img_number),
                    image.original.path.replace('original', 'web')
                )
                shutil.copy2(
                    os.path.join(os.path.dirname(__file__), 'test-data', '%s-thumb.jpg' % img_number),
                    image.original.path.replace('original', 'thumb')
                )
