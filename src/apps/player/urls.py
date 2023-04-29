from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('homepage', views.index, name='index'),
    # path('new_releases'),
    # path('chart'),
    # """music urls for user"""
    path('playlists', views.playlists, name='playlists'),
    path('tracks', views.tracks, name='tracks'),
    # path('artists', views.artists, name='artists'),
    path('history', views.history, name='history'),

    path('chats', views.chats, name='chats'),

    path('userpage', views.userpage, name='userpage'),
    # path('settings/account'),
    # path('settings/other')
]
