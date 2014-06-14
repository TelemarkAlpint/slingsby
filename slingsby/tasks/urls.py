from django.conf.urls import patterns

urlpatterns = patterns('slingsby.tasks',
    (r'^update_archive', 'update_archive.update_archive'),
)
