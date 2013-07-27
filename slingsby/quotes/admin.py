from .models import Quote
from django.contrib import admin
from django.forms.models import ModelForm

class AdminQuoteForm(ModelForm):
    class Meta:
        model = Quote

class QuoteAdmin(admin.ModelAdmin):
    form = AdminQuoteForm
    readonly_fields = ('date_added', )

admin.site.register(Quote, QuoteAdmin)
