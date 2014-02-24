class HttpAcceptMiddleware(object):
    """ Parse the HTTP_ACCEPT header and add two attributes to the request object,
     `prefer_html` and `prefer_json`.

    An empty accept header means by the spec that the client can recieve any kind of response,
    so we default to html in that case.
    """

    def process_request(self, request):
        content_types = request.META.get('HTTP_ACCEPT')
        content_types = content_types.split(',') if content_types else []
        accepts = {}
        for item in content_types:
            params = item.split(';')
            media_type = params.pop(0)
            priority = 1.0
            for param in params:
                key, val = param.split('=')
                if key == 'q':
                    priority = float(val)
                    continue
            accepts[media_type] = priority

        # If not json or html requested explicitly, default to html
        if not ('application/json' in accepts or 'text/html' in accepts):
            accepts['text/html'] = 1.0

        request.prefer_html = bool(accepts.get('text/html', 0) >= accepts.get('application/json', 0))
        request.prefer_json = bool(accepts.get('application/json', 0) > accepts.get('text/html', 0))


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
