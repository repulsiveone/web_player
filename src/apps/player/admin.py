from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm, ListWTrack, UserTrack
from .models import CustomUser, TrackList, UserMusic


class CustomUserAdmin(UserAdmin):
    ass_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'username']


class TrackListAdmin(admin.ModelAdmin):
    form = ListWTrack
    model = TrackList
    list_display = ['id', 'name', 'duration', 'location']


class UserMusicAdmin(admin.ModelAdmin):
    form = UserTrack
    model = UserMusic
    list_display = ['user', 'track']


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(TrackList, TrackListAdmin)
admin.site.register(UserMusic, UserMusicAdmin)
