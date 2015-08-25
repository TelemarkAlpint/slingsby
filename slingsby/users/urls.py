# coding: utf-8

from .views import UserProfileView, LogoutView, JoinView
from django.conf.urls import url
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^profil$', login_required(UserProfileView.as_view()), name='profile'),
    url(r'^profil/resend', login_required(UserProfileView.as_view()), name='resend-email'), # TODO: Implement
    url(r'^blimed$', login_required(JoinView.as_view()), name='signup'),
    url(r'^meldut$', login_required(UserProfileView.as_view()), name='leave-group'), # TODO: Implement
    url(r'^logout$', LogoutView.as_view(), name='logout'),
]
