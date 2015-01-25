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
                if key == 'action':
                    if not initkwargs[key] in getattr(cls, 'actions', ()):
                        raise TypeError(u"%s.as_view() received an invalid action '%s', possible "
                            "actions are %s" % (cls.__name__, initkwargs[key],
                                getattr(cls, 'actions')))
                else:
                    raise TypeError(u"%s.as_view() received an invalid keyword %r" % (
                        cls.__name__, key))

        def view(request, *args, **kwargs):
            self = cls(**initkwargs)
            if hasattr(self, 'get') and not hasattr(self, 'head'):
                self.head = self.get
            self.request = request
            self.args = args
            self.kwargs = kwargs

            # This line added to original implementation
            self.action = initkwargs.get('action')

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

        # if action is not set, this should just behave like a normal view
        if not self.action:
            return super(ActionView, self).dispatch(request, *args, **kwargs)

        if request.method.lower() == 'post':
            handler = getattr(self, self.action, self.action_not_implemented)
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)


    def _allowed_methods(self):
        if self.action:
            return ['POST', 'OPTIONS']
        else:
            return super(ActionView, self)._allowed_methods()


    def action_not_implemented(self, request, *args, **kwargs):
        raise NotImplementedError('You requested an URL with an action %s that has not been '
            'implemented yet' % self.action)
