# coding: utf-8
# pylint: disable=unpacking-non-sequence

from ..general import make_title
from ..general.mixins import JSONMixin
from .models import Event, Image, EventForm
from .tasks import process_image

from datetime import datetime
from django.core.files.images import get_image_dimensions
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView
from logging import getLogger
from PIL import Image as PILImage

_logger = getLogger(__name__)

class ArchiveView(TemplateView):

    template_name = 'archive/archive_list.html'

    def get_context_data(self, **kwargs):
        context = super(ArchiveView, self).get_context_data(**kwargs)
        events = [e for e in Event.objects.all() if e.images]
        context['events'] = events
        context['title'] = make_title('Arkiv')
        context['event_form'] = EventForm()
        context['show_event'] = int(self.request.GET.get('showEvent', '0'))
        return context


    def post(self, request, **kwargs):
        if not request.user.has_perm('archive.can_upload_images'):
            return HttpResponseForbidden()

        form = EventForm(request.POST)
        context = self.get_context_data(**kwargs)
        uploaded_images = request.FILES.getlist('images')
        photographer = request.POST.get('photographer', '')
        if form.is_valid() and uploaded_images:
            year = form.data['startdate'].split('-')[0]
            existing_event = Event.objects.filter(startdate__contains=year, name__iexact=form.data['name'])
            event = existing_event[0] if existing_event else form.save()
            for image in uploaded_images:
                image_id = save_uploaded_image(event, image, photographer)
                process_image.delay(image_id)
            messages.info(request, 'Bildene ble lastet opp, vennligst vent mens vi nedskalerer dem og ' +
                'flytter dem over på filserveren, kom tilbake snart!')
            return HttpResponseRedirect(reverse('archive'))
        else:
            messages.warning(request, 'Oops, ser ut til at du har noen feil i opplastingsskjemaet, prøv ' +
                'en gang til!')
            context['event_form'] = form
            return self.render_to_response(context, status=400)


def get_image_capture_time(image):
    """ Extract the capture time from the EXIF of a image, or return None if nothing was found. """
    # EXIF data is on the format (id, value), the ID for "DateTimeOriginal", ie. the capture time,
    # is 36867
    datetimeoriginal = 36867
    try:
        img = PILImage.open(image)
        if hasattr(img, '_getexif'):
            exifinfo = img._getexif() # pylint: disable=protected-access
            if exifinfo != None:
                datestring = exifinfo.get(datetimeoriginal)
                if datestring and not datestring == '0000:00:00 00:00:00':
                    return datetime.strptime(datestring, '%Y:%m:%d %H:%M:%S')
    except Exception: # pylint: disable=broad-except
        _logger.exception('Error occured extracting capture time from image: %s', image)
    return None


def save_uploaded_image(event, uploaded_image, photographer):
    width, height = get_image_dimensions(uploaded_image)
    capture_time = get_image_capture_time(uploaded_image)
    if not capture_time:
        capture_time = datetime.utcnow()
    image = Image(
        original=uploaded_image,
        original_filename=uploaded_image.name,
        original_height=height,
        original_width=width,
        datetime_taken=capture_time,
        event=event,
        photographer=photographer,
    )
    _logger.info('Saving new uploaded image %s (%dx%d)', image, height, width)
    image.save()
    return image.id


class EventDetailView(JSONMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = super(EventDetailView, self).get_context_data(**kwargs)
        event_id = kwargs['event_id']
        event = get_object_or_404(Event, pk=event_id)
        context['event'] = event
        return context


    def get_json(self, request, **kwargs):
        context = self.get_context_data(**kwargs)
        event = context['event']
        return {'event': event.to_json()}
