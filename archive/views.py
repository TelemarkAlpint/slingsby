# coding: utf-8

from archive.models import ArchiveEvent, ImageGallery, Image, Video
from contextlib import closing
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.views.generic.simple import direct_to_template
from general import make_title, cache
from general.constants import JSON_ARCHIVE_PATH
from general.cache import CachedQuery
from urllib2 import urlopen
import datetime
import json
import logging

class ArchiveEventQuery(CachedQuery):
    queryset = ArchiveEvent.objects.all()

def view_archive(request):
    events = ArchiveEventQuery.get_cached()
    values = {
              'events': events,
              'title': make_title('Arkiv')
              }
    return direct_to_template(request, 'archive/archive_list.html', values)

def event_details(request, event_id):
    event = get_object_or_404(ArchiveEvent, pk=event_id)
    return render_to_response('archive/event_details.html', {'event': event})

def update_archive(request):
    logging.info('Starting to update archive event database')
    if 'clear_all' in request.GET and request.user.is_staff:
        logging.info('Deleting all old entries')
        clear_archive_and_cache()
    archive = get_archive()
    logging.info('JSON archive fetched.')
    old_hashes = get_old_hashes()
    logging.info('Old hashes found, creating new events...')
    new_hashes = create_new_events(archive, old_hashes)
    logging.info('All new items created.')
#    delete_old_events(all_db_events, old_hashes - new_hashes)
    return HttpResponseRedirect(reverse('archive'))

def clear_archive_and_cache():
    """ Delete all ArchiveEvents, ImageGalleries and Images, and flush the cache."""

    logging.info('Deleting all old events')
    for event in ArchiveEvent.objects.all():
        event.delete()
    logging.info('Deleting all old galleries')
    for gallery in ImageGallery.objects.all():
        gallery.delete()
    logging.info('Deleting all old images')
    for image in Image.objects.all():
        image.delete()
    cache.flush_all()

def get_archive():
    with closing(urlopen(JSON_ARCHIVE_PATH)) as fp:
        return json.load(fp)

def get_old_hashes():
    hashes = ArchiveEvent.objects.values_list('path_hash', flat=True)
    return set(hashes)

def create_and_get_events(archive, old_hashes):
    images = []
    for path_hash, event in archive['events'].items():
        if path_hash not in old_hashes:
            e = ArchiveEvent()
            e.date = event['date']
            e.name = event['name']
            e.path_hash = path_hash
            e.save()
            logging.info('New event found: %s', e.name)
        else:
            e = ArchiveEvent.objects.get(pk=path_hash)
        old_galleries = set(ImageGallery.objects.values_list('path_hash', flat=True))
        for gallery_hash, gallery in event['galleries'].items():
            if not gallery['images']:
                continue
            if gallery_hash not in old_galleries:
                g = ImageGallery()
                g.path_hash = gallery_hash
                g.photographer = gallery['photographer']
                g.event = e
                g.save()
                logging.info('New gallery for event "%s" found: %s', e.name, g.photographer)
            else:
                g = ImageGallery.objects.get(pk=gallery_hash)
            old_images = set(Image.objects.values_list('path_hash', flat=True))
            for img_hash, img in gallery['images'].items():
                if img_hash not in old_images:
                    i = Image()
                    i.path_hash = img_hash
                    i.medium_size_url = img['websize']
                    i.large_size_url = img['fullsize']
                    i.gallery = g
                    i.description = img.get('description', None)
                    images.append(i)
            if not g.cover_photo:
                img_hash, cover_img = gallery['images'].popitem()
                g.cover_photo = cover_img['websize']
                g.save()
    Image.objects.bulk_create(images)

def create_new_events(archive, old_hashes):
    """ Save all objects to the database which is not present in the old hash set.

    Returns the hashes of all the new objects. """

    create_and_get_events(archive, old_hashes)

def delete_old_events(events, hashes):
    for event in events:
        if event.data_hash in hashes:
            logging.info('Deleted outdated event: %s' % event)
            event.delete()