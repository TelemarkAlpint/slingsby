from ..general.templatetags.revved_static import get_revved_url

from django.forms.widgets import Textarea

class SocialSummaryWidget(Textarea):

    custom_attrs = {
        'cols': 80,
        'rows': 3,
        'class': 'social_summary_textbox'
    }

    def __init__(self):
        super(SocialSummaryWidget, self).__init__(self.custom_attrs)


    class Media:
        js = (
            get_revved_url('js/socialSummary.min.js') or 'js/socialSummary.min.js',
        )
