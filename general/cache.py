from abc import ABCMeta, abstractproperty
from google.appengine.api import memcache
import logging
import os

# Current version prepended to every keyword, to prevent mixup of the caches between different versions
_PREFIX = os.environ.get('CURRENT_VERSION_ID', '')

"""
Due to some funky coding from Google, all of the memcache functions will show a warning in Eclipse. Partly due
to that, and partly to provide a common gateway to the memcache, this module exists. From here it's also
possible to log what's put into the cache, if that should prove necessary for debugging reasons.
"""

logger = logging.getLogger(__name__)

def set(keyword, obj, timeout=None): #@ReservedAssignment
    key = _PREFIX + keyword
    if timeout is None:
        memcache.set(key, obj) #@UndefinedVariable
    else:
        memcache.set(key, obj, timeout) #@UndefinedVariable
        logger.debug('Element added to cache: %s -> %s.' % (key, str(obj)[:150]))

def get(keyword):
    key = _PREFIX + keyword
    fetched_obj = memcache.get(key) #@UndefinedVariable
    logger.debug('Element fetched from cache: %s -> %s.' % (key, str(fetched_obj)[:150]))
    return fetched_obj

def flush_all():
    memcache.flush_all() #@UndefinedVariable

def delete(keyword):
    key = _PREFIX + keyword
    memcache.delete(key) #@UndefinedVariable
    logger.debug('Deleted from cache: %s' % key)

class CachedQuery(object):
    """ A wrapper class for querysets that should be cached.

    Usage:

    >>>class SampleQuery(CachedQuery):
    >>>    queryset = MyObject.objects.filter(date__gte>now)

    >>>objects = SampleQuerySet.get_cached()

    Subclasses must override the queryset property. Optional properties is timeout_in_s,
    for specifying the max time the query will stay in the cache. For debugging purposes,
    subclasses can define a property do_not_cache=True, which will turn off caching for that query.

    To automatically refresh the queryset in case a model is changed, add the following line:
    >>>post_save.connect(SampleQuery.empty_on_save, sender=MyObject)

    This can also be accomplished by specifying a property parent_model. The CachedQuery
    will then do the connect itself.
    """

    __metaclass__ = ABCMeta

    @abstractproperty
    def queryset(self):
        pass

    do_not_cache = False
    timeout_in_s = None
    parent_model = None

    @classmethod
    def update_cache(cls, objects=None):
        """ Fetch the latest queryset from the db, and put it into the cache.

        If objects is given, those will be put into the cache. """

        if objects is None:
            objects = cls.queryset.all()
        if cls.timeout_in_s:
            set(cls.__name__, objects, cls.timeout_in_s)
        else:
            set(cls.__name__, objects)
        return objects

    @classmethod
    def get_cached(cls):
        """ Pull out what's found in the cache, if empty, return a fresh queryset. """

        if cls.do_not_cache:
            return cls.queryset.all()
        objects = get(cls.__name__)
        if objects is not None:
            return objects
        else:
            return cls.update_cache()

    @classmethod
    def empty_cache(cls):
        delete(cls.__name__)

    @classmethod
    def empty_on_save(cls, sender, instance=None, **kwargs):
        logger.debug('Clearing cached query: %s.' % cls.__name__)
        cls.empty_cache()

