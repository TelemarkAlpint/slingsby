from django.conf.urls import patterns, url

urlpatterns = patterns('quotes.views',
      url('^$', 'all_quotes', name='all_quotes'),
      url('^upload$', 'upload_quote', name='upload_quote'),
      url(r'^(\d+)/$', 'show_quote', name='show_quote'),
      url(r'^(\d+)/approve/$', 'approve_quote', name='approve_quote'),
      url(r'^(\d+)/delete/$', 'delete_quote', name='delete_quote'),
      )