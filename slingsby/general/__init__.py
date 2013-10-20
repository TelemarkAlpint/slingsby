from bs4 import BeautifulSoup
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.safestring import mark_safe
from django.views.generic import TemplateView
import logging

_LEGAL_TAGS = set(['p', 'br', 'ol', 'li', 'ul', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'img', 'a',
                  'b', 'strong', 'italic', 'i', 'em', 'div', 'iframe', 'table', 'tr', 'th', 'td',
                  'tbody', 'thead', 'tfoot', 'span', 'q', 'blockquote', 'dd', 'dl', 'dt'])

def append_slash(request, page):
    return HttpResponseRedirect('/%s/' % page)


class NotYetImplementedView(TemplateView):
    template_name = 'infopage.html'

    def get_context_data(self):
        return {'content': 'Beklager, men denne funksjonen har vi ikke implementert enda.'}


def validate_text(text):
    raw = BeautifulSoup(text)
    illegal_tags = []
    for tag in raw.findAll(True):
        if tag.name not in _LEGAL_TAGS:
            illegal_tags.append(tag)
    if illegal_tags:
        logging.warning('Validation failed for text.')
        logging.warning('Illegal tags found: ' + ', '.join([tag.name for tag in illegal_tags]))
        logging.warning('Contexts: ' + '\n'.join(str(tag) for tag in illegal_tags))
        raise ValidationError('Illegal tags found: ' + ', '.join([tag.name for tag in illegal_tags]))
    return raw.prettify()

def make_title(subpage=None):
    if subpage:
        return '%s :: NTNUI Telemark/Alpint' % subpage
    else:
        return 'NTNUI Telemark/Alpint'
