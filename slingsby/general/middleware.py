class HttpAcceptMiddleware(object):
    """ Parse the HTTP_ACCEPT header and add it to the request object.

    Also adds two convenience attributes to the request, prefer_html and prefer_json, which what
    format the browser would like to recieve the response as.
    The format of the http_accept is [("Mime-type", {"key": value}, priority)], orderer by priority.
    """

    def process_request(self, request):
        content_types = request.META.get('HTTP_ACCEPT', '').split(',')
        accepts = []
        json_priority = 0.0
        html_priority = 0.0
        for item in content_types:
            params = item.split(';')
            media_type = params.pop(0)
            priority = 1.0
            param_dict = {}
            for param in params:
                key, val = param.split('=')
                if key == 'q':
                    priority = float(val)
                else:
                    param_dict[key] = val
            if media_type == 'application/json':
                json_priority = priority
            elif media_type == 'text/html':
                html_priority = priority
            accepts.append( (media_type, param_dict, priority))
        accepts.sort(lambda x, y: -cmp(x[2], y[2]))
        request.http_accept = accepts
        request.prefer_html = html_priority > json_priority
        request.prefer_json = json_priority > html_priority

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
