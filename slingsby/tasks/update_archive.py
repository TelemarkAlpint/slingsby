"""
This entire module is bad bad bad and should be migrated away from.

A much better solution would be for the file server to push changes to a
RESTful interface to the archive, with some sort of authentication to ensure
everything comes from the fileserver. Then we can set up a proper file manager
at the fileserver, with browsing, editing and deleting of files. Eventually
flip that around, and expose a RESTful interface to the fileserver for modifying
files, but I'm assuming it's more effective the other way around (to avoid having
to transfer files first to the webserver and then forward to the fileserver).

Anyway, the key to working with large datasets like these -> bulk_create!

"""

from django.http import HttpResponse
from logging import getLogger

_logger = getLogger(__name__)

def update_archive(request):
    """ Check the fileserver for the archive JSON, and create new events from that.

    NOTE: Does not delete old entries that has been removed from the JSON!
    """
    _logger.info('Starting to update archive event database')
    # if 'clear_all' in request.GET and request.user.is_staff:
    #     _logger.info('Deleting all old entries')
    #     clear_archive_and_cache()
    archive = requests.get(JSON_ARCHIVE_PATH).json()
    _logger.info('JSON archive fetched.')
    new_hashes = create_and_get_events(archive)
    _logger.info('All new items created.')
#    delete_old_events(all_db_events, old_hashes - new_hashes)
    return HttpResponse()


# def clear_archive_and_cache():
#     """ Delete all ArchiveEvents, ImageGalleries and Images, and flush the cache."""

#     logging.info('Deleting all old events')
#     for event in ArchiveEvent.objects.all():
#         event.delete()
#     logging.info('Deleting all old galleries')
#     for gallery in ImageGallery.objects.all():
#         gallery.delete()
#     logging.info('Deleting all old images')
#     for image in Image.objects.all():
#         image.delete()
#     cache.flush_all()


def create_and_get_events(archive):
    """ Iterate through the archive JSON and create new event objects for all
    events not present in the set of old hashes. Also check for each event
    whether there are any new galleries, and for every gallery whether there
    are new images.
    """
    old_event_hashes = set(ArchiveEvent.objects.values_list('path_hash', flat=True))
    images = []
    for path_hash, event in archive['events'].items():
        if path_hash not in old_event_hashes:
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


# def delete_old_events(events, hashes):
#     for event in events:
#         if event.data_hash in hashes:
#             _logger.info('Deleted outdated event: %s', event)
#             event.delete()
