from django.contrib import auth
from django.utils.functional import SimpleLazyObject
from general import cache

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
            q = 1.0
            param_dict = {}
            for param in params:
                key, val = param.split('=')
                if key == 'q':
                    q = float(val)
                else:
                    param_dict[key] = val
            if media_type == 'application/json':
                json_priority = q
            elif media_type == 'text/html':
                html_priority = q
            accepts.append( (media_type, param_dict, q))
        accepts.sort(lambda x, y: -cmp(x[2], y[2]))
        request.http_accept = accepts
        request.prefer_html = html_priority > json_priority
        request.prefer_json = json_priority > html_priority


class CachedAuthMiddleware(object):
    """ Store session user in cache, to avoid hitting the database on every pageview. """

    @staticmethod
    def get_user(request):
        user_id = request.session.get('_auth_user_id')
        if user_id is None:
            user = auth.get_user(request)
        else:
            user = cache.get('auth_user-%d' % user_id)
            if user is None:
                user = auth.get_user(request)
                cache.set('auth_user-%d' % user_id, user)
        return user

    def process_request(self, request):
        assert hasattr(request, 'session'), "The CachedAuthMiddleware requires the django.contrib.sessions.middleware.SessionMiddleware to be installed!"
        request.user = SimpleLazyObject(lambda: CachedAuthMiddleware.get_user(request))