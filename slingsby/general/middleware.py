# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.messages.api import MessageFailure
from django.shortcuts import redirect
from django.utils.http import urlquote
from social.exceptions import SocialAuthBaseException, AuthCanceled
from social.apps.django_app.middleware import (
    SocialAuthExceptionMiddleware as _SocialAuthExceptionMiddleware)
import collections
import hotshot
import hotshot.stats
import httpheader
import logging
import os
import re
import six
import StringIO
import sys
import tempfile

_logger = logging.getLogger(__name__)

def _get_qvalue(accept_types, content_type_string):
    content_type = httpheader.content_type(content_type_string)
    class_qvalue = None
    universal_wildcard_qvalue = None
    ret = 0
    for accept_content_type, qvalue, _ in accept_types:
        if accept_content_type == content_type:
            ret = qvalue
            break
        elif accept_content_type.is_wildcard() and accept_content_type.major == content_type.major:
            class_qvalue = qvalue
        elif accept_content_type.is_universal_wildcard():
            universal_wildcard_qvalue = qvalue
    else:
        if class_qvalue is not None:
            ret = class_qvalue
        if universal_wildcard_qvalue is not None:
            ret = universal_wildcard_qvalue
    return ret


class HttpAcceptMiddleware(object):
    """ Parse the HTTP_ACCEPT header and add two attributes to the request object,
     `prefer_html` and `prefer_json`.

    An empty accept header means by the spec that the client can recieve any kind of response,
    so we default to html in that case.
    """

    def process_request(self, request):
        accept_header = request.META.get('HTTP_ACCEPT')
        if accept_header:
            try:
                accept_types = httpheader.parse_accept_header(accept_header)
                # print('Parsed headers: %s' % accept_types)
                # from nose.tools import set_trace as f; f()
            except httpheader.ParseError:
                _logger.warning('Failed to parse HTTP Accept header, was %s', accept_header)
                html_qvalue = 1
                json_qvalue = 0
            else:
                html_qvalue = _get_qvalue(accept_types, 'text/html')
                json_qvalue = _get_qvalue(accept_types, 'application/json')
        else:
            html_qvalue = 1
            json_qvalue = 0

        # If not json or html requested explicitly, default to html
        if html_qvalue == 0 and json_qvalue == 0:
            html_qvalue = 1

        request.prefer_html = html_qvalue >= json_qvalue
        request.prefer_json = not request.prefer_html


class HttpMethodOverride(object):
    """ HTML has no way of sending HTTP DELETE or PUT requests. To patch up this,
    we allow the specification of desired HTTP verb in the _http_verb request data
    field. If the request is a POST request and has this field, the value from that
    field will override the original HTTP request verb.
    """

    def process_request(self, request):
        if request.method == 'POST':
            if request.POST.get('_http_verb'):
                request.method = request.POST.get('_http_verb')




# Orignal version taken from http://www.djangosnippets.org/snippets/186/
# Original author: udfalkso
# Modified by: Shwagroo Team and Gun.io
WORDS_RE = re.compile(r'\s+')

GROUP_PREFIXES = [
    re.compile("^.*/django/[^/]+"),
    re.compile("^(.*)/[^/]+$"), # extract module path
    re.compile(".*"),           # catch strange entries
]

class ProfileMiddleware(object):
    """
    Displays hotshot profiling for any view.
    http://yoursite.com/yourview/?prof

    Add the "prof" key to query string by appending ?prof (or &prof=)
    and you'll see the profiling results in your browser.
    It's set up to only be available in django's debug mode, is available for superuser otherwise,
    but you really shouldn't add this middleware to any production configuration.

    WARNING: It uses hotshot profiler which is not thread safe.
    """
    def process_request(self, request):
        # pylint: disable=attribute-defined-outside-init
        if (settings.DEBUG or request.user.is_superuser) and 'prof' in request.GET:
            self.tmpfile = tempfile.mktemp()
            self.prof = hotshot.Profile(self.tmpfile)

    def process_view(self, request, callback, callback_args, callback_kwargs):
        if (settings.DEBUG or request.user.is_superuser) and 'prof' in request.GET:
            return self.prof.runcall(callback, request, *callback_args, **callback_kwargs)

    def get_group(self, filename):
        for group_prefix in GROUP_PREFIXES:
            name = group_prefix.findall(filename)
            if name:
                return name[0]

    def get_summary(self, results_dict, total):
        items = sorted(results_dict.items(), key=lambda t: (t[1], t[0]), reverse=True)

        res = ["      tottime"]
        for module, time in items[:40]:
            res.append("%4.1f%% %7.3f %s" % (100*time/total if total else 0, time, module))

        return '\n'.join(res)

    def _extract_filename_from_line_spec(self, line_spec):
        """ A line spec is either on the form
            "/path/to/module.py:<linenum>(<func_name>)"
        on linux, or
            "<drive_letter>:\\path\\to\\module.py:<linenum>(<func_name>)"
        on windows. This func extracts /path/to/module.py from both forms.
        """
        parts = line_spec.split(':')
        if len(parts) == 3:
            # windows-style path
            return parts[1].replace('\\', '/')
        else:
            return parts[0]

    def summary_for_files(self, stats_str):
        stats_str = stats_str.split("\n")[5:]

        mystats = collections.defaultdict(int)
        mygroups = collections.defaultdict(int)

        total = 0

        for stat in stats_str:
            fields = WORDS_RE.split(stat)
            if len(fields) == 7:
                time = float(fields[2])
                total += time
                filename = self._extract_filename_from_line_spec(fields[6])

                if time:
                    mystats[filename] += time

                    group = self.get_group(filename)
                    mygroups[group] += time

        return ("<pre>"
               " ---- By file ----\n\n%s\n"
               " ---- By group ---\n\n%s"
               "</pre>") % (self.get_summary(mystats, total), self.get_summary(mygroups, total))

    def process_response(self, request, response):
        if (settings.DEBUG or request.user.is_superuser) and 'prof' in request.GET:
            self.prof.close()

            out = StringIO.StringIO()
            old_stdout = sys.stdout
            sys.stdout = out

            stats = hotshot.stats.load(self.tmpfile)
            stats.sort_stats('time', 'calls')
            stats.print_stats()

            sys.stdout = old_stdout
            stats_str = out.getvalue()

            if response and response.content and stats_str:
                response.content = "<h1>Profiling results</h1><pre>" + stats_str + "</pre>"

            response.content = "\n".join(response.content.split("\n")[:40])

            response.content += self.summary_for_files(stats_str)

            os.unlink(self.tmpfile)

        return response


class SocialAuthExceptionMiddleware(_SocialAuthExceptionMiddleware):
    """Middleware that handles Social Auth AuthExceptions by providing the user
    with a message, logging an error, and redirecting to some next location.

    By default, the exception message itself is sent to the user and they are
    redirected to the location specified in the SOCIAL_AUTH_LOGIN_ERROR_URL
    setting.

    NTNUITA: Overriden from what's included in python-social-auth to not show message back
    to user as error, but as warning. Also redirects back to the page the user was on when
    initializing the authentication, instead of root.

    Note: This can be tested by using one of the Facebook test users and aborting the auth, go to
    https://developers.facebook.com/apps/1416174671936188/roles/test-users/ to manage them.
    """

    def process_exception(self, request, exception):
        strategy = getattr(request, 'social_strategy', None)
        if strategy is None or self.raise_exception(request, exception):
            return

        if isinstance(exception, SocialAuthBaseException):
            backend = getattr(request, 'backend', None)
            backend_name = getattr(backend, 'name', 'unknown-backend')

            message = self.get_message(request, exception)
            _logger.warning('Auth cancelled by user')

            url = self.get_redirect_uri(request, exception) or '/'
            try:
                messages.warning(request, message,
                               extra_tags='social-auth ' + backend_name)
            except MessageFailure:
                url += ('?' in url and '&' or '?') + \
                       'message={0}&backend={1}'.format(urlquote(message),
                                                        backend_name)
            return redirect(url)


    def get_message(self, request, exception):
        if isinstance(exception, AuthCanceled):
            return 'Autentisering avbrutt, prøv igjen om du ombestemmer deg.'
        return six.text_type(exception)


    def get_redirect_uri(self, request, exception):
        strategy = getattr(request, 'social_strategy', None)
        if strategy:
            next_param = strategy.session_get(REDIRECT_FIELD_NAME)
            if next_param:
                return next_param
            return strategy.setting('LOGIN_ERROR_URL')
