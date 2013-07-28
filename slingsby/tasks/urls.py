from django.conf.urls import patterns

urlpatterns = patterns('slingsby.tasks',
    (r'^update_archive', 'update_archive.update_archive'),
    (r'^count_votes', 'count_votes.update_ratings'),
    (r'^empty_cache', 'empty_vote_cache.empty_cache'),
)
