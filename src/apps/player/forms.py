from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, TrackList


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
        fields = ('name', 'duration', 'location')


# class ListWTrackChange(forms.ModelForm):
#     class Meta:
#         model = TrackList
#         fields = ('name', 'duration')
