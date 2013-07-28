from ..general import make_title
from ..general.cache import CachedQuery, empty_on_changes_to
from .models import Gear
from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView

@empty_on_changes_to(Gear)
class AllGearQuery(CachedQuery):
    queryset = Gear.objects.all()


class GearListView(TemplateView):

    template_name = 'gear/gear_list.html'

    def get_context_data(self, **kwargs):
        context = super(GearListView, self).get_context_data(**kwargs)
        all_gear = AllGearQuery.get_cached()
        context['all_gear'] = all_gear
        context['title'] = make_title('Utleie')
        return context


    def get(self, request, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class GearDetailView(TemplateView):

    template_name = 'gear/gear_details.html'

    def get_context_data(self, **kwargs):
        context = super(GearDetailView, self).get_context_data(**kwargs)
        gear_id = kwargs['gear_id']
        gear = get_object_or_404(Gear, id=gear_id)
        context['gear'] = gear
        context['title'] = make_title(gear.gear_id)
        return context


    def get(self, request, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)
