from bs4 import BeautifulSoup
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.safestring import mark_safe
from django.utils.html import strip_tags
from django.views.generic import TemplateView
from logging import getLogger

_logger = getLogger('slingsby.general')

_LEGAL_TAGS = set(['p', 'br', 'ol', 'li', 'ul', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'img', 'a',
                  'b', 'strong', 'italic', 'i', 'em', 'div', 'iframe', 'table', 'tr', 'th', 'td',
                  'tbody', 'thead', 'tfoot', 'span', 'q', 'blockquote', 'dd', 'dl', 'dt'])


def validate_text(text):
    raw = BeautifulSoup(text)
    illegal_tags = []
    for tag in raw.findAll(True):
        if tag.name not in _LEGAL_TAGS:
            illegal_tags.append(tag)
    if illegal_tags:
        _logger.warning('Validation failed for text.')
        _logger.warning('Illegal tags found: ' + ', '.join([tag.name for tag in illegal_tags]))
        _logger.warning('Contexts: ' + '\n'.join(str(tag) for tag in illegal_tags))
        raise ValidationError('Illegal tags found: ' + ', '.join([tag.name for tag in illegal_tags]))
    return raw.prettify()


def make_title(subpage=None):
    if subpage:
        return '%s :: NTNUI Telemark-Alpint' % strip_tags(subpage)
    else:
        return 'NTNUI Telemark-Alpint'
