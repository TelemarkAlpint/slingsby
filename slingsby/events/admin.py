from .models import Event, EventForm, Signup
from django.contrib import admin

class SignupInline(admin.TabularInline):
    model = Signup

class EventAdmin(admin.ModelAdmin):
    form = EventForm
    ordering = ['-startdate']
    inlines = [
        SignupInline,
    ]

admin.site.register(Event, EventAdmin)
admin.site.register(Signup)
