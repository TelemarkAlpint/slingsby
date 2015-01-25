from django.views.generic.base import View
from django.utils.decorators import classonlymethod
from functools import update_wrapper

# pylint: disable=attribute-defined-outside-init

class ActionView(View):
    """ A view that in addition to dispatching to methods get, post, delete, etc.,
    also dispatches to methods defined on the objects as actions, as a tuple of
    allowed action.

    Example:

    class SongDetailView(ActionView):
        actions = ('vote', 'approve')

        def vote(self, request, **kwargs):
            ...

    In your URLConf, you'd then do this to dispatch requests to this view:
    url(r'^(?P<song_id>\\d+)/vote/$', SongDetailView.as_view(action='vote')
    """
    # Pylint doesn't catch on to the classonlymethod decorator:
    # pylint: disable=no-self-argument,not-callable


    @classonlymethod
    def as_view(cls, **initkwargs):
        """
        Main entry point for a request-response process.

        Function mostly copied from the django source for the View class, only added a few lines.
        """
        # sanitize keyword arguments
        for key in initkwargs:
            if key in cls.http_method_names:
                raise TypeError(u"You tried to pass in the %s method name as a "
                                u"keyword argument to %s(). Don't do that."
                                % (key, cls.__name__))
            if not hasattr(cls, key):
                # These two lines was added to the original source:
                valid_action = key == 'action' and initkwargs[key] in getattr(cls, 'actions', ())
                if not valid_action:
                    raise TypeError(u"%s() received an invalid keyword %r" % (
                        cls.__name__, key))

        def view(request, *args, **kwargs):
            self = cls(**initkwargs)
            if hasattr(self, 'get') and not hasattr(self, 'head'):
                self.head = self.get
            # These two lines added to original source:
            if 'action' in initkwargs:
                kwargs['action'] = initkwargs['action']
            return self.dispatch(request, *args, **kwargs)

        # take name and docstring from class
        update_wrapper(view, cls, updated=())

        # and possible attributes set by decorators
        # like csrf_exempt from dispatch
        update_wrapper(view, cls.dispatch, assigned=())
        return view


    def dispatch(self, request, *args, **kwargs):
        # Try to dispatch to the right method; if a method doesn't exist,
        # defer to the error handler. Also defer to the error handler if the
        # request method isn't on the approved list.

        action = kwargs.get('action')
        if action and not request.method.lower() == 'post':
            handler = self.http_method_not_allowed
        elif request.method.lower() == 'post' and action in self.actions:
            handler = getattr(self, kwargs['action'])
        elif action is None and request.method.lower() in self.http_method_names:
            #from nose.tools import set_trace as f; f()
            handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        self.request = request
        self.args = args
        self.kwargs = kwargs
        return handler(request, *args, **kwargs)
