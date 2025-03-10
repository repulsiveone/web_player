"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.player.urls')),
    path('homepage/', include('apps.player.urls')),
    path('signup/', include('apps.player.urls')),
    path('login/', include('apps.player.urls')),
    path('logout/', include('apps.player.urls')),
    path('tracks/', include('apps.player.urls')),
    path('playlists/', include('apps.player.urls')),
    path('playlist/<int:id>/', include('apps.player.urls')),
    path('select_playlist/', include('apps.player.urls')),
    path('load/', include('apps.player.urls')),
    path('delete_track/', include('apps.player.urls')),
    path('add_track_to_playlist/', include('apps.player.urls')),
    path('create_playlist/', include('apps.player.urls')),
    path('playlist_add_to_user/', include('apps.player.urls')),
    path('playlist_delete_from_user/', include('apps.player.urls')),
    path('track_all_playlists/', include('apps.player.urls')),
    path('edit_playlist/<int:id>', include('apps.player.urls')),
]
