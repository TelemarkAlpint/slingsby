from django.conf.urls import patterns, url

urlpatterns = patterns('musikk.views',
    url(r'^$', 'all_songs', name='musikk'),
    url(r'^(\d+)/$', 'song_details', name='song_details'),
    url(r'^(\d+)/vote/$', 'vote_on_song', name='vote_on_song'),
    url(r'^(\d+)/approve/$', 'approve_song', name='approve_song'),
    url(r'^(\d+)/delete/$', 'delete_song', name='delete_song'),
    url(r'^top/list/$', 'top_list', name='top_list'),
    url(r'^top/song/$', 'top_song', name='top_song'),
    (r'^top/$', 'top'),
    (r'^upload_song$', 'upload_song'),
)