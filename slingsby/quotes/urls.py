from .views import AllQuotesView, QuoteDetailView
from django.conf.urls import url
from django.contrib.admin.views.decorators import staff_member_required

urlpatterns = [
    url('^$', AllQuotesView.as_view(), name='all_quotes'),
    url(r'^/(?P<quote_id>\d+)$', QuoteDetailView.as_view(), name='show_quote'),
    url(r'^/(?P<quote_id>\d+)/approve$', staff_member_required(QuoteDetailView.as_view(action='approve')),
        name='approve_quote'),
]
