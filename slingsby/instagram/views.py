from .models import InstagramMedia
from ..general import make_title

from django.views.generic.base import TemplateView

class AllInstagramMediaView(TemplateView):

    template_name = 'instagram/all.html'

    def get(self, request, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


    def get_context_data(self, **kwargs):
        context = super(AllInstagramMediaView, self).get_context_data(**kwargs)
        context['all_media'] = InstagramMedia.objects.filter(visible=True)
        context['title'] = make_title('Instagram')
        return context
