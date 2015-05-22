"""
This module implements a class you should extend when creating queries than
should be cached.

If necessary, you may also inject cache debugging code here.
"""
# pylint: disable=redefined-builtin

from abc import ABCMeta, abstractproperty
from django.core.cache import cache
from django.db.models.query import ValuesQuerySet
from django.db.models.signals import post_save, post_delete
from logging import getLogger
import os

_logger = getLogger(__name__)

def empty_on_changes_to(model):
    """ A decorator that might be used on CachedQueries to empty them
    on changes to a model. Will connect the query to both post_save and
    post_delete of the given model.
    """

    def class_wrapper(cls):
        _logger.debug("Connecting model %s to query %s", model, cls)
        post_save.connect(cls.empty_on_save, sender=model)
        post_delete.connect(cls.empty_on_save, sender=model)
        return cls

    return class_wrapper


class CachedQuery(object):
    """ A wrapper class for querysets that should be cached.

    Usage:

    >>> class SampleQuery(CachedQuery):
    >>>   queryset = MyObject.objects.filter(date__gte>now)

    >>> objects = SampleQuerySet.get_cached()

    Subclasses must override the queryset property. Optional properties is timeout_in_s,
    for specifying the max time the query will stay in the cache. For debugging purposes,
    subclasses can define a property do_not_cache=True, which will turn off caching for that query.

    To automatically refresh the queryset in case a model is changed, add the following line:
    >>> post_save.connect(SampleQuery.empty_on_save, sender=MyObject)

    This can also be accomplished by specifying a property parent_model. The CachedQuery
    will then do the connect itself.
    """

    __metaclass__ = ABCMeta

    do_not_cache = False
    timeout_in_s = None
    parent_model = None

    @abstractproperty
    def queryset(self):
        pass


    @classmethod
    def update_cache(cls, objects=None):
        """ Fetch the latest queryset from the db, and put it into the cache.

        If objects is given, those will be put into the cache. """

        if objects is None:
            # Force get fresh from db
            objects = cls.queryset.all()
            if isinstance(objects, ValuesQuerySet):
                # This line is necessary to allow serializing ValuesQuerySets
                objects = [item for item in objects]
        if cls.timeout_in_s:
            cache.set(cls.__name__, objects, cls.timeout_in_s)
        else:
            cache.set(cls.__name__, objects)
        return objects


    @classmethod
    def get_cached(cls):
        """ Pull out what's found in the cache, if empty, return a fresh queryset. """

        if cls.do_not_cache:
            return cls.queryset.all()
        objects = cache.get(cls.__name__)
        if objects is not None:
            return objects
        else:
            return cls.update_cache()


    @classmethod
    def empty_cache(cls):
        cache.delete(cls.__name__)


    @classmethod
    def empty_on_save(cls, sender, instance=None, **kwargs):
        _logger.debug('Clearing cached query: %s.', cls.__name__)
        cls.empty_cache()
