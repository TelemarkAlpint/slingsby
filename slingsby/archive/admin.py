from .models import Event, Image, ImageForm

from django.contrib import admin

class ImageAdmin(admin.ModelAdmin):
    form = ImageForm
    readonly_fields = (
        'original_height',
        'original_width',
        'original_filename',
    )

admin.site.register(Event)
admin.site.register(Image, ImageAdmin)
