from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, BaseUserCreationForm
from .models import CustomUser, TrackList, UserMusic


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email')


class TrackListForm(forms.ModelForm):
    class Meta:
        model = TrackList
        fields = ('id', 'name', 'duration', 'location')


class UserMusicForm(forms.ModelForm):
    class Meta:
        model = UserMusic
        fields = ('user', 'track')


class SignUpForm(BaseUserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')


class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = CustomUser
        fields = ('email', 'password')
