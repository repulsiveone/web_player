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
    path('history', views.history, name='history'),

    path('chat/', views.chat, name='chats'),
    path('chat/<str:room_name>/', views.room, name='room'),

    path('userpage', views.userpage, name='userpage'),
    # path('settings/account'),
    # path('settings/other')
]
