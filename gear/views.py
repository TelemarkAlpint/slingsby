from django.db.models.signals import post_save
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.views.generic.simple import direct_to_template
from gear.models import Gear
from general import make_title
from general.cache import CachedQuery
import json

class AllGearQuery(CachedQuery):
    queryset = Gear.objects.all()

post_save.connect(AllGearQuery.empty_on_save, sender=Gear)

def all_gear(request):
    all_gear = AllGearQuery.get_cached()
    if request.prefer_json:
        json_array = [gear.__json__() for gear in all_gear]
        return HttpResponse(json.dumps(json_array), mimetype='application/json')
    context = {
               'all_gear': all_gear,
               'title': make_title('Utleie'),
               }
    return direct_to_template(request, 'gear/all_gear.html', context)

def gear_details(request, gear_id):
    gear = get_object_or_404(Gear, id=gear_id)
    if request.prefer_json:
        return HttpResponse(json.dumps(gear.__json__()), mimetype='application/json')
    context = {
               'gear': gear,
               'title': make_title(gear.gear_id),
               }
    return direct_to_template(request, 'gear/gear_details.html', context)

@require_POST
def gear_reservation(request, gear_id):
    pass