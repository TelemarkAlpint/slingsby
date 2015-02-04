from .views import GearListView, GearDetailView
from django.conf.urls import patterns, url

urlpatterns = patterns('',
      url(r'^$', GearListView.as_view(), name='all_gear'),
      url(r'^/(?P<gear_id>\d+L?)$', GearDetailView.as_view(), name='gear_details'),
      #url(r'^(?P<gear_id>\d+L?)/book$', 'gear_reservation', name='gear_reservation'),
      )
