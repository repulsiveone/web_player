from django.http import FileResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
import json
from .models import TrackList, CustomUser, UserMusic, Playlist
from .forms import SignUpForm, AuthenticationForm, LoginForm
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse


""" main page with player """
# def index(request):

    # return render(request, 'app/index.html')


"""1: вывод плейлиста из базы в список и отправка в джс
   2: id += 1 и отправка в функцию джанго и вызов с бд
   можно сделать разные id для треков и отдельные id в плейлистах для корректного вывода"""


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            """работает но не логинит"""
            user = form.save()
            playlist = Playlist.objects.create(name='favorite', user=user)
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=password)
            login(request, user)

            return redirect('/login')

    else:
        form = SignUpForm()
    return render(request, 'app/signup.html', {'form': form})


def log_in(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/homepage')
    else:
        form = LoginForm()

    return render(request, 'app/login.html', {'form': form})

"""главная страница где по умолчанию плейлист favorite для пользователя"""

"""нужно сделать чтобы при авторизации пользователя, ему создавался плейлист favorite и выбор этого плейлиста, для главной страницы"""
def index(request):
    if request.method == 'POST':
        current_user = request.user
        """получить пользователя, запрос к плейлистам по id пользователю и по названию favorite, это будет current playlist"""
        """работает"""
        current_playlist = Playlist.objects.get(user=current_user, name='favorite')

        current_playlist_data = {
            'name': current_playlist.name,
            'tracks': [],
        }

        for track in current_playlist.tracks.all():
            track_data = {
                'title': track.name,
                'audio_path': track.location,
            }

            current_playlist_data['tracks'].append(track_data)

        return JsonResponse(current_playlist_data, content_type='application/json')

    return render(request, 'app/homepage.html')


"""выбор плейлиста по нажатию по id"""
def select_playlist(request):
    """get потому что с ajax передаю??"""
    if request.method == "POST":
        current_playlist_id = request.POST.get('playlist_id')
        current_playlist = Playlist.objects.get(id=current_playlist_id)

        current_playlist_data = {
            'name': current_playlist.name,
            'tracks': [],
        }

        for track in current_playlist.tracks.all():
            track_data = {
                'title': track.name,
                'audio_path': track.location,
            }

            current_playlist_data['tracks'].append(track_data)

        return JsonResponse(current_playlist_data)


def update_playlist(playlist):
    current_playlist_data = {
        'name': playlist.name,
        'tracks': [],
    }

    for track in playlist.tracks.all():
        track_data = {
            'title': track.name,
            'audio_path': track.location,
        }

        current_playlist_data['tracks'].append(track_data)

    return JsonResponse(current_playlist_data)


def add_track(request):
    if request.method == "POST":
        track_id = request.POST.get('track_id')
        track = TrackList.objects.get(id=track_id)
        playlist_id = request.POST.get('playlist_id')
        playlist = Playlist.objects.get(id=playlist_id)
        playlist.tracks.add(track)
        playlist.save()
        update_playlist(playlist)


def delete_track(request):
    if request.method == "POST":
        track_id = request.POST.get('track_id')
        track = TrackList.objects.get(id=track_id)
        playlist_id = request.POST.get('playlist_id')
        playlist = Playlist.objects.get(id=playlist_id)
        playlist.tracks.remove(track)
        playlist.save()
        update_playlist(playlist)


def tracks(request):
    if request.method == "POST":
        pass
    #todo надо переделать базу данных / добавить плейлист/user и убрать usermusic
    current_user = request.user
    current_playlist = Playlist.objects.get(user=current_user, name='favorite')

    current_playlist_data = {
        'name': current_playlist.name,
        'tracks': [],
    }

    for track in current_playlist.tracks.all():
        track_data = {
            'title': track.name,
            'audio_path': track.location,
        }

        current_playlist_data['tracks'].append(track_data)
    # 'WSGIRequest' object has no attribute 'is_ajax'
    # if request.is_ajax():
    #     return JsonResponse(current_playlist_data, content_type='application/json')

    return render(request, 'app/user_music.html', {'fav_playlist': current_playlist_data})


def playlists(request):
    if request.method == "POST":
        pass
    current_user = request.user

    list_playlists = []

    us_playlists = Playlist.objects.filter(user=current_user)

    for playlist in us_playlists:
        user_playlists = {
            'name': playlist.name,
            'tracks': [],
        }

        for track in playlist.tracks.all():
            track_data = {
                'title': track.name,
                'audio_path': track.location,
            }

            user_playlists['tracks'].append(track_data)
        list_playlists.append(user_playlists)
    # 'WSGIRequest' object has no attribute 'is_ajax'
    # if request.is_ajax():
    #     return JsonResponse(list_playlists, content_type='application/json')
    return render(request, 'app/user_playlists.html', {'playlists': list_playlists})


def top_playlists(request):
    pass


def history(request):
    pass


def chats(request):
    pass


def userpage(request):
    pass


def setting(request):
    pass
