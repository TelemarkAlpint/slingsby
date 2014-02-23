from .time import utc_to_nor
from django.contrib.admin import widgets
from django.forms.widgets import Textarea
from datetime import datetime

class NORDateTimeWidget(widgets.AdminSplitDateTime):

    def render(self, name, value, attrs=None):
        if isinstance(value, datetime):
            utcdate = value
            nordate = utc_to_nor(utcdate)
            return super(NORDateTimeWidget, self).render(name, nordate, attrs)
        else:
            return super(NORDateTimeWidget, self).render(name, value, attrs)


class WidgEditorWidget(Textarea):

    custom_attrs = {
        'cols': 80,
        'rows': 10,
        'class': 'widgEditor nothing',
    }

    def __init__(self):
        super(WidgEditorWidget, self).__init__(self.custom_attrs)


    class Media:
        js = ('js/widgEditor.min.js',)
        css = {
            'all': ('stylesheets/widgEditor.css',)
        }
