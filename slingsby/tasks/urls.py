from django.conf.urls import patterns

urlpatterns = patterns('slingsby.tasks',
    (r'^sync_users$', 'sync_users.sync_users'),
    (r'^sync_profile_img$', 'sync_users.sync_profile_images'),
    (r'^find_names$', 'profiles.add_name_where_missing'),
    (r'^update_archive', 'update_archive.update_archive'),
    (r'^count_votes', 'count_votes.update_ratings'),
    (r'^empty_cache', 'empty_vote_cache.empty_cache'),
)
