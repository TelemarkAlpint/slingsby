from django.contrib import admin
from django.forms.models import ModelForm
from quotes.models import Quote

class AdminQuoteForm(ModelForm):
    class Meta:
        model = Quote

class QuoteAdmin(admin.ModelAdmin):
    form = AdminQuoteForm
    readonly_fields = ('date_added', )

admin.site.register(Quote, QuoteAdmin)