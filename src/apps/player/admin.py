from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm, ListWTrack
from .models import CustomUser, TrackList


class CustomUserAdmin(UserAdmin):
    ass_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'username']


class TrackListAdmin(admin.ModelAdmin):
    form = ListWTrack
    model = TrackList
    list_display = ['name', 'duration', 'location']


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(TrackList, TrackListAdmin)
