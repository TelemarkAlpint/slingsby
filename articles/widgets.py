from django.contrib.admin import widgets
from django.forms.widgets import Textarea
from general.time import utc_to_nor
from datetime import datetime

class NORDateTimeWidget(widgets.AdminSplitDateTime):
    def render(self, name, value, attrs=None):
        if isinstance(value, datetime):
            utcdate = value
            nordate = utc_to_nor(utcdate)
            return super(NORDateTimeWidget, self).render(name, nordate, attrs)
        else:
            return super(NORDateTimeWidget, self).render(name, value, attrs)

class SocialSummaryWidget(Textarea):
    custom_attrs={'cols': 80, 'rows': 3,
                  'class': 'social_summary_textbox'}

    def __init__(self):
        super(SocialSummaryWidget, self).__init__(self.custom_attrs)

    class Media:
        js = ('js/jquery-1.8.1.min.js', 'js/socialSummary.js')
