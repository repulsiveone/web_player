from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm, TrackListForm, UserMusicForm, PlaylistForm
from .models import CustomUser, TrackList, UserMusic, Playlist


class UserMusicInline(admin.TabularInline):
    model = UserMusic


class CustomUserAdmin(UserAdmin):
    ass_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'username']

    filter_horizontal = ('track',)

    inlines = [UserMusicInline]


class TrackListAdmin(admin.ModelAdmin):
    form = TrackListForm
    model = TrackList
    list_display = ['id', 'name', 'duration', 'location']


class UserMusicAdmin(admin.ModelAdmin):
    form = UserMusicForm
    model = UserMusic
    list_display = ['user', 'track']


class PlaylistAdmin(admin.ModelAdmin):
    form = PlaylistForm
    model = Playlist


admin.site.register(Playlist, PlaylistAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(TrackList, TrackListAdmin)
admin.site.register(UserMusic, UserMusicAdmin)
