# coding: utf-8

from ..general import make_title
from ..general.cache import CachedQuery, empty_on_changes_to
from .models import ArchiveEvent
from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView

@empty_on_changes_to(ArchiveEvent)
class ArchiveEventQuery(CachedQuery):
    queryset = ArchiveEvent.objects.all()


class ArchiveView(TemplateView):

    template_name = 'archive/archive_list.html'

    def get_context_data(self, **kwargs):
        context = super(ArchiveView, self).get_context_data(**kwargs)
        events = ArchiveEventQuery.get_cached()
        context['events'] = events
        context['title'] = make_title('Arkiv')
        return context


class ArchiveEventDetailView(TemplateView):

    template_name = 'archive/event_details.html'

    def get_context_data(self, **kwargs):
        context = super(ArchiveEventDetailView, self).get_context_data(**kwargs)
        event_id = kwargs['event_id']
        event = get_object_or_404(ArchiveEvent, pk=event_id)
        context['event'] = event
        return context
