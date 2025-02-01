from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, BaseUserCreationForm, AuthenticationForm
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from .models import CustomUser, TrackList, UserMusic, Playlist, PlaylistTracks



import unicodedata

import os
from django import forms
from django.contrib.auth import authenticate, get_user_model, password_validation
from django.contrib.auth.hashers import UNUSABLE_PASSWORD_PREFIX, identify_hasher
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.mail import EmailMultiAlternatives
from django.template import loader
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.text import capfirst
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _
UserModel = get_user_model()


class MaxFileSizeValidator:
    def __init__(self, max_size):
        self.max_size = max_size

    def __call__(self, file):
        if file.size > self.max_size:
            raise ValidationError(f"Максимальный размер файла должен быть {self.max_size} байтов.")


class MP3FileValidator:
    def __call__(self, file):
        ext = os.path.splitext(file.name)[1]
        if ext.lower() != '.mp3':
            raise ValidationError("Файл должен быть в формате MP3.")


class ImageFileValidator:
    def __call__(self, file):
        ext = os.path.splitext(file.name)[1]
        if ext.lower() != '.jpg' and ext.lower() != '.png':
            raise ValidationError("Файл должен быть в формате jpg или png.")



class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email')


class TrackListForm(forms.Form):
    MAX_FILE_SIZE = 20 * 1024 * 1024

    track_file = forms.FileField(label='Выберите аудио файл',
                                 validators=[MaxFileSizeValidator(MAX_FILE_SIZE), MP3FileValidator()])
    track_image = forms.FileField(label='Выберите обложку',
                                  validators=[MaxFileSizeValidator(MAX_FILE_SIZE), ImageFileValidator()], required=False)
    track_title = forms.CharField(label='', max_length=100, required=False, widget=forms.TextInput(
        attrs={'style': "width: 600px; border-radius: 5px; padding: 10px; top: 100%; left: 40%; transform: translate(40%, 100%);", 'placeholder': "Название трека"}))
    track_author = forms.CharField(label='', max_length=100, required=False, widget=forms.TextInput(
        attrs={'style': "width: 600px; border-radius: 5px; padding: 10px; top: 150%; left: 40%; transform: translate(40%, 150%);", 'placeholder': "Имя исполнителя"}))

    def clean_track_title(self):
        title = self.cleaned_data.get('track_title')
        if not title:
            title = 'untitled'
            self.cleaned_data['track_title'] = title
        return title

    def clean_track_author(self):
        author = self.cleaned_data.get('track_author')
        if not author:
            author = 'unknown'
            self.cleaned_data['track_author'] = author
        return author

    def clean_track_image(self):
        image = self.cleaned_data.get('track_image')
        if not image:
            image = '/static/default_image_for_track.jpg'
            self.cleaned_data['track_image'] = image
        return image

    # class Meta:
    #     model = TrackList
    #     fields = ('name', 'location', 'author', 'image')


class UserMusicForm(forms.ModelForm):
    class Meta:
        model = UserMusic
        fields = ('user', 'playlist')

    
class PlaylistTracksForm(forms.ModelForm):
    class Meta:
        model = PlaylistTracks
        fields = ('playlist', 'track', 'order_id')


class SignUpForm(UserCreationForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(
        attrs={'class': 'container form-control', 'style': "width: 300px; ", 'placeholder': 'username'}))
    email = forms.EmailField(label='Email', required=True, widget=forms.TextInput(
        attrs={'class': 'container form-control', 'style': "width: 300px; ", 'placeholder': 'email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'container form-control', 'style': "width: 300px;", 'placeholder': 'password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'container form-control', 'style': "width: 300px;", 'placeholder': 'password'}))

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')


class LoginForm(AuthenticationForm):
    username = forms.EmailField(label='Email', required=True, widget=forms.TextInput(
        attrs={'class': 'container form-control', 'style': "width: 300px; ", 'placeholder': 'email'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'container form-control', 'style': "width: 300px;", 'placeholder': 'password'}))

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('username')

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist: #работает но все равно подсвечивается
            self.add_error('username', 'Неправильный адрес электронной почты')
            return

        cleaned_data['email'] = user

        return cleaned_data


class PlaylistForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = ('id', 'name', 'user', 'tracks')

