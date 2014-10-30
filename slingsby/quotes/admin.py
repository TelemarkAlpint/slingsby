from .models import Quote
from django.contrib import admin


class QuoteAdmin(admin.ModelAdmin):
    readonly_fields = ('date_added', )

    def has_add_permission(self, request):
        """ Add quotes from the normal interface from the main site, not from the admin site. """
        return False


admin.site.register(Quote, QuoteAdmin)
