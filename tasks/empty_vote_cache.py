from django.http import HttpResponse
from general import cache
from musikk.views import AllReadySongsCache, TopSongsCache

def empty_cache(request):
    cache.delete('vote_dict')
    AllReadySongsCache.empty_cache()
    TopSongsCache.empty_cache()
    return HttpResponse()