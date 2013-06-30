from django.contrib import admin
from users.models import UserProfile, NameLookup

admin.site.register(UserProfile)
admin.site.register(NameLookup)