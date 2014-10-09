from .models import Event, EventForm
from django.contrib import admin

class EventAdmin(admin.ModelAdmin):
    form = EventForm
    ordering = ['-startdate']

admin.site.register(Event, EventAdmin)
