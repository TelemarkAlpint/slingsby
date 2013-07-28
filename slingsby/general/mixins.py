from django.http import HttpResponse
import json

class JSONMixin(object):

    def dispatch(self, request, *args, **kwargs):
        # Try to dispatch to the right method; if a method doesn't exist,
        # defer to the error handler. Also defer to the error handler if the
        # request method isn't on the approved list.
        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(), self.http_method_not_allowed)

        else:
            handler = self.http_method_not_allowed
        self.request = request
        self.args = args
        self.kwargs = kwargs

        # If the request wants JSON, return handler get_json or post_json, etc.
        # Expect the method to return a dict that can be passed to json.dumps
        if request.prefer_json and request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower() + '_json', handler)
            json_data = handler(request, *args, **kwargs)
            return HttpResponse(json.dumps(json_data), mimetype='application/json')
        return handler(request, *args, **kwargs)
