from django.core.files.storage import FileSystemStorage
from django.http import FileResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
import json
from .models import TrackList, CustomUser, UserMusic, Playlist
from .forms import SignUpForm, AuthenticationForm, LoginForm, TrackListForm
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse, HttpResponse


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

    return render(request, 'app/homepage.html')


# for /homepage and /tracks.
def default_playlist(request):
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
            'path': track.location,
            'image': track.image,
        }

        current_playlist_data['tracks'].append(track_data)
    print(current_playlist_data)
    return JsonResponse(current_playlist_data)


"""выбор плейлиста по нажатию по id"""
def select_playlist(request):
    current_user = request.user
#     """get потому что с ajax передаю??"""
    playlist_id = request.GET.get('id')
    print(playlist_id)
    current_playlist = UserMusic.objects.get(user=current_user, id=playlist_id)

    current_playlist_data = {
        'name': current_playlist.playlist.name,
        'tracks': [],
    }

    for track in current_playlist.playlist.tracks.all():
        track_data = {
            'title': track.name,
            'path': track.location,
            'image': track.image,
            'author': track.author,
        }

        current_playlist_data['tracks'].append(track_data)

    print(current_playlist_data)

    return JsonResponse(current_playlist_data)


# def update_playlist(playlist):
#     current_playlist_data = {
#         'name': playlist.name,
#         'tracks': [],
#     }
#
#     for track in playlist.tracks.all():
#         track_data = {
#             'title': track.name,
#             'audio_path': track.location,
#         }
#
#         current_playlist_data['tracks'].append(track_data)
#
#     return JsonResponse(current_playlist_data)
#
#
# def add_track(request):
#     if request.method == "POST":
#         track_id = request.POST.get('track_id')
#         track = TrackList.objects.get(id=track_id)
#         playlist_id = request.POST.get('playlist_id')
#         playlist = Playlist.objects.get(id=playlist_id)
#         playlist.tracks.add(track)
#         playlist.save()
#         update_playlist(playlist)
#
#
# def delete_track(request):
#     if request.method == "POST":
#         track_id = request.POST.get('track_id')
#         track = TrackList.objects.get(id=track_id)
#         playlist_id = request.POST.get('playlist_id')
#         playlist = Playlist.objects.get(id=playlist_id)
#         playlist.tracks.remove(track)
#         playlist.save()
#         update_playlist(playlist)


def tracks(request):
    current_user = request.user
    playlist = Playlist.objects.get(user=current_user, name='favorite')

    return render(request, 'app/user_music.html', {'playlist': playlist})


def playlists(request):
    current_user = request.user

    list_playlists = UserMusic.objects.filter(user=current_user)

    return render(request, 'app/user_playlists.html', {'playlists': list_playlists})


def playlist_tracks(request, id):
    user_playlist = UserMusic.objects.get(id=id)
    if request.method == "POST":
        current_playlist = Playlist.objects.get(id=user_playlist.playlist.id)

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

    playlist = Playlist.objects.get(id=user_playlist.playlist.id)

    return render(request, 'app/playlist_tracks.html', {'id': id, 'playlist': playlist})


def top_playlists(request):
    pass


def load_track(request):
    current_user = request.user
    if request.method == "POST":
        form = TrackListForm(request.POST, request.FILES)
        #todo """media root настроить чтобы файлы сохранялись в разные места"""
        if form.is_valid():
            data = form.cleaned_data
            track_file = request.FILES['track_file']
            track_image = request.FILES['track_image']
            """добавление пути в базу и автоматическое добавление в плейлист fav для current user"""
            fs = FileSystemStorage()
            filename_track_file = fs.save(track_file.name, track_file)
            filename_track_image = fs.save(track_image.name, track_image)

            track_list = TrackList(name=data['track_title'], location=f"/static/{filename_track_file}",
                                   author=data['track_author'], image=f"/static/{filename_track_image}")
            track_list.save()

            user_favorite_playlist = Playlist.objects.get(user=current_user, name='favorite')
            user_favorite_playlist.tracks.add(track_list)
            user_favorite_playlist.save()

            return redirect('/load')
        else:
            pass
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
