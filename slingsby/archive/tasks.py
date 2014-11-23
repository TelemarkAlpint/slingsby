from ..general.utils import (log_errors, fileserver_ssh_client, upload_file_to_fileserver, slugify,
    ignored)
from .models import Image

from celery import shared_task
from django.conf import settings
from logging import getLogger
from PIL import Image as PILImage, ImageOps
from pilkit.processors import ResizeToFit
from pilkit.utils import save_image
import os

_logger = getLogger(__name__)

@shared_task
@log_errors
def process_image(image_id):
    """ Create a websize and thumbnail image from an uploaded image, upload them and the original
    to the fileserver, mark the image as ready and delete the local version.
    """
    files_to_transfer = None
    image = None
    try:
        image = Image.objects.get(pk=image_id)
        if not image:
            raise ValueError('No image with id %d found.' % image_id)
        _logger.info('Processing image %s at %s', image.id, image.original)
        files_to_transfer = create_resizes_of_image(image)
        with fileserver_ssh_client() as ssh_client:
            for src, dest in files_to_transfer:
                upload_file_to_fileserver(ssh_client, src, dest)
        image.ready = True
        image.save()
        _logger.info("New image #%d processed successfully", image.id)
    except Exception: # pylint: disable=broad-except
        if image:
            image.delete()
        raise
    finally:
        if files_to_transfer:
            for src, _ in files_to_transfer:
                with ignored(OSError):
                    os.remove(src)


def create_resizes_of_image(image):
    """ Create the web and thumb, and return a list of (source, dest) images to be transferred to
    the fileserver, including the original.
    """
    event = image.event
    year = event.startdate.split('-')[0]
    dest_media_folder = '/'.join(['archive', year, slugify(event.name)])

    # Add original to files to be transferred
    files_to_transfer = [
        (image.original.path, '/'.join([dest_media_folder, '%d-original.jpg' % image.id]))
    ]

    # Do the actual conversion
    pil_img = PILImage.open(image.original)
    thumb = ImageOps.fit(pil_img, (75, 75), PILImage.ANTIALIAS)
    #thumb = ResizeToFit(75, 75).process(pil_img)
    websize = ResizeToFit(1500, 800, upscale=False).process(pil_img)
    for size, appendix in [(thumb, 'thumb'), (websize, 'web')]:
        filename = '%s-%s.jpg' % (image.id, appendix)
        local_path = os.path.join(settings.MEDIA_ROOT, 'temp-archive-images', filename)
        if not os.path.exists(os.path.dirname(local_path)):
            os.mkdir(os.path.dirname(local_path))
        save_image(size, local_path, 'jpeg')
        files_to_transfer.append(
            (local_path, '/'.join([dest_media_folder, filename]))
        )

    # Set the new URL to the original image
    image.original = None
    image.original = dest_media_folder + '/%d-original.jpg' % image.id

    return files_to_transfer
