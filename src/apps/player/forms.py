from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, TrackList, UserMusic


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email')


class ListWTrack(forms.ModelForm):
    class Meta:
        model = TrackList
        fields = ('id', 'name', 'duration', 'location')


class UserTrack(forms.ModelForm):
    class Meta:
        model = UserMusic
        fields = ('user', 'track')


# class ListWTrackChange(forms.ModelForm):
#     class Meta:
#         model = TrackList
#         fields = ('name', 'duration')
