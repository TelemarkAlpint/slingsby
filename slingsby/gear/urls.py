from django.conf.urls import patterns, url

urlpatterns = patterns('slingsby.gear.views',
      url(r'^$', 'all_gear', name='all_gear'),
      url(r'^(\d+L?)/$', 'gear_details', name='gear_details'),
      url(r'^(\d+L?)/book$', 'gear_reservation', name='gear_reservation'),
      )