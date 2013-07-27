from django.contrib import admin
from archive.models import ArchiveEvent, ImageGallery, \
    Video, Image

admin.site.register(ArchiveEvent)
admin.site.register(ImageGallery)
admin.site.register(Image)
admin.site.register(Video)
