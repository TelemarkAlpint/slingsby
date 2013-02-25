from events.models import Event, EventForm
from django.contrib import admin

class EventAdmin(admin.ModelAdmin):
    form = EventForm

admin.site.register(Event, EventAdmin)
