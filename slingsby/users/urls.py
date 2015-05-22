# coding: utf-8

from .views import UserProfileView, LogoutView
from django.conf.urls import url
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^profil$', login_required(UserProfileView.as_view()), name='profile'),
    url(r'^logout$', LogoutView.as_view(), name='logout'),
]
