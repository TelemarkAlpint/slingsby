from archive.views import update_archive
from django.http import HttpResponse

def update(request):
    update_archive(request)
    return HttpResponse()

def clear_and_update(request):
    return HttpResponse()
