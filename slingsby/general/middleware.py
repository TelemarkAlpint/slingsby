import hotshot
import hotshot.stats
import httpheader
import logging
import os
import re
import StringIO
import sys
import tempfile

from django.conf import settings

_logger = logging.getLogger(__name__)

def _get_qvalue(accept_types, content_type_string):
    content_type = httpheader.content_type(content_type_string)
    class_qvalue = None
    universal_wildcard_qvalue = None
    for accept_content_type, qvalue, extensions in accept_types:
        if accept_content_type == content_type:
            return qvalue
        elif accept_content_type.is_wildcard() and accept_content_type.major == content_type.major:
            class_qvalue = qvalue
        elif accept_content_type.is_universal_wildcard():
            universal_wildcard_qvalue = qvalue

    if class_qvalue is not None:
        return class_qvalue
    if universal_wildcard_qvalue is not None:
        return universal_wildcard_qvalue
    return 0


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
words_re = re.compile(r'\s+')

group_prefix_re = [
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
        if (settings.DEBUG or request.user.is_superuser) and 'prof' in request.GET:
            self.tmpfile = tempfile.mktemp()
            self.prof = hotshot.Profile(self.tmpfile)

    def process_view(self, request, callback, callback_args, callback_kwargs):
        if (settings.DEBUG or request.user.is_superuser) and 'prof' in request.GET:
            return self.prof.runcall(callback, request, *callback_args, **callback_kwargs)

    def get_group(self, file):
        for g in group_prefix_re:
            name = g.findall(file)
            if name:
                return name[0]

    def get_summary(self, results_dict, sum):
        list = [(item[1], item[0]) for item in results_dict.items()]
        list.sort(reverse=True)
        list = list[:40]

        res = "      tottime\n"
        for item in list:
            res += "%4.1f%% %7.3f %s\n" % (100*item[0]/sum if sum else 0, item[0], item[1])

        return res

    def summary_for_files(self, stats_str):
        stats_str = stats_str.split("\n")[5:]

        mystats = {}
        mygroups = {}

        sum = 0

        for s in stats_str:
            fields = words_re.split(s);
            if len(fields) == 7:
                time = float(fields[2])
                sum += time
                file = fields[6].split(":")[0]

                if not file in mystats:
                    mystats[file] = 0
                mystats[file] += time

                group = self.get_group(file)
                if not group in mygroups:
                    mygroups[group] = 0
                mygroups[group] += time

        return "<pre>" + \
               " ---- By file ----\n\n" + self.get_summary(mystats, sum) + "\n" + \
               " ---- By group ---\n\n" + self.get_summary(mygroups, sum) + \
               "</pre>"

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
                response.content = "<pre>" + stats_str + "</pre>"

            response.content = "\n".join(response.content.split("\n")[:40])

            response.content += self.summary_for_files(stats_str)

            os.unlink(self.tmpfile)

        return response
