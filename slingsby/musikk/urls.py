from .views import SongDetailView, AllSongsView, TopSongsView, TopSong, TopSongsList
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

urlpatterns = patterns('',
    url(r'^$', AllSongsView.as_view(), name='musikk'),

    url(r'^(?P<song_id>\d+)/$', SongDetailView.as_view(), name='song_details'),
    url(r'^(?P<song_id>\d+)/vote/$', login_required(SongDetailView.as_view(action='vote')), name='vote_on_song'),
    url(r'^(?P<song_id>\d+)/approve/$', staff_member_required(SongDetailView.as_view(action='approve')), name='approve_song'),

    url(r'^top/$', TopSongsView.as_view()),
    url(r'^top/list/$', TopSongsList.as_view(), name='top_list'),
    url(r'^top/song/$', TopSong.as_view(), name='top_song'),
)
