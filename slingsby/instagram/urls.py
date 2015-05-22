from .views import AllInstagramMediaView

from django.conf.urls import url

urlpatterns = [
    url(r'^$', AllInstagramMediaView.as_view(), name='all_instagram'),
]
