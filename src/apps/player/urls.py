from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('homepage/', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.log_in, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    # """music urls for user"""
    path('playlists/', views.playlists, name='playlists'),
    path('tracks/', views.tracks, name='tracks'),
    path('playlist/<int:id>/', views.playlist_tracks, name='playlist'),
    path('history', views.history, name='history'),
    path('select_playlist/', views.select_playlist, name='select_playlist'),

    path('chats', views.chats, name='chats'),

    path('delete_track/', views.delete_track, name='delete_track'),
    path('add_track_to_playlist/', views.add_track_to_playlist, name='add_track_to_playlist'),
    path('playlist_add_to_user/', views.playlist_add_to_user, name='playlist_add_to_user'),
    path('playlist_delete_from_user/', views.playlist_delete_from_user, name='playlist_delete_from_user'),
    path('track_all_playlists/', views.track_all_playlists, name='track_all_playlists'),
    path('edit_playlist/<int:id>/', views.edit_playlist, name='edit_playlist'),

    path('userpage', views.userpage, name='userpage'),
    path('load/', views.load_track, name='load_track'),
    path('create_playlist/', views.create_playlist, name='create_playlist'),
    # path('settings/account'),
    # path('settings/other')
]
