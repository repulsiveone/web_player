from django.core.files.storage import FileSystemStorage
from django.http import FileResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
import json
from .models import TrackList, CustomUser, UserMusic, Playlist
from .forms import SignUpForm, AuthenticationForm, LoginForm, TrackListForm
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
def index(request):
    if request.method == 'POST':
        current_user = request.user
        current_playlist = Playlist.objects.get(user=current_user, name='favorite')
        """на этой странице не нужно название плейлиста и тд, нужна вся информация про треки"""
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

"""если play то с ajax как то и чтобы id отправлялся а если список треков то просто выводится но наверное получается также по нажатию"""
def playlists(request):
    if request.method == "POST":
        pass
    current_user = request.user

    list_playlists = []

    us_playlists = UserMusic.objects.filter(user=current_user)

    for playlist in us_playlists:
        user_playlists = {
            'name': playlist.playlist.name,
            'tracks': [],
        }

        for track in playlist.playlist.tracks.all():
            track_data = {
                'title': track.name,
                'audio_path': track.location,
            }

            user_playlists['tracks'].append(track_data)
        list_playlists.append(user_playlists)
    # 'WSGIRequest' object has no attribute 'is_ajax'
    """добавить просто в if POST и отправлять в ajax"""
    # if request.is_ajax():
    #     return JsonResponse(list_playlists, content_type='application/json')
    return render(request, 'app/user_playlists.html', {'playlists': list_playlists})


def top_playlists(request):
    pass


def load_track(request):
    if request.method == "POST":
        form = TrackListForm(request.POST, request.FILES)
        if form.is_valid():
            track_file = request.FILES['track_file']
            track_image = request.FILES['track_image']
            """сделать чтобы файлы не сохранялись дважды (redirect)"""
            """добавление пути в базу и автоматическое добавление в плейлист fav для current user"""
            """вроде сохраняется в папку"""
            fs = FileSystemStorage()
            filename = fs.save(track_file.name, track_file)
            uploaded_file_url = fs.url(filename)
            print(uploaded_file_url)

            print('valid')
        else:
            print('not valid')
    else:
        form = TrackListForm()
    return render(request, 'app/load_track.html', {'form': form})


def history(request):
    pass


def chats(request):
    pass


def userpage(request):
    pass


def setting(request):
    pass
