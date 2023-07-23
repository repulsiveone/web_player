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
    current_user = request.user
    if request.method == 'POST':
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
        return JsonResponse(current_playlist_data, content_type='application/json')

    playlist = Playlist.objects.get(user=current_user, name='favorite')

    return render(request, 'app/homepage.html', {'playlist': playlist})


"""выбор плейлиста по нажатию по id"""
# def select_playlist(request):
#     """get потому что с ajax передаю??"""
#     if request.method == "POST":
#         current_playlist_id = request.POST.get('playlist_id')
#         current_playlist = Playlist.objects.get(id=current_playlist_id)
#
#         current_playlist_data = {
#             'name': current_playlist.name,
#             'tracks': [],
#         }
#
#         for track in current_playlist.tracks.all():
#             track_data = {
#                 'title': track.name,
#                 'audio_path': track.location,
#             }
#
#             current_playlist_data['tracks'].append(track_data)
#
#         return JsonResponse(current_playlist_data)


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


def test_json(request):
    track_list = [{'title': 'NICHEVO', 'audio_path': '/static/Kai_Angel_9mice_-_N1CHEVO_75442759_rrTGxEE.mp3', 'path': '/static/Kai_Angel_9mice_-_N1CHEVO_75442759_rrTGxEE.mp3', 'image': '/static/moGD5CaUq8g.jpg' , 'author': 'kai'},
                  {'title': 'paris', 'audio_path': '/static/Kai_Angel_-_PARIS_2008_76293616_iOrfeKA.mp3', 'path': '/static/Kai_Angel_-_PARIS_2008_76293616_iOrfeKA.mp3', 'image': '/static/moGD5CaUq8g_ick7wx1.jpg', 'author': 'kai'},
                  {'title': 'липстик', 'audio_path': '/static/Kai_Angel_9mice_-_LIPSTICK_75442758_7GqYUye.mp3', 'path': '/static/Kai_Angel_9mice_-_LIPSTICK_75442758_7GqYUye.mp3', 'image': '/static/moGD5CaUq8g_HYc3Rnq.jpg', 'author': 'kai'},
                  {'title': 'Stargirl_Interlude', 'audio_path': '/static/Lana_Del_Rey_The_Weeknd_-_Stargirl_Interlude_47829074.mp3', 'path': '/static/Lana_Del_Rey_The_Weeknd_-_Stargirl_Interlude_47829074.mp3', 'image': '/static/bd40e40dc8f0e5638c17b42ac3bcdff0_oKZT3gi.jpg', 'author': 'the weeknd'},
                  {'title': 'Blinding_Lights', 'audio_path': '/static/The_Weeknd_-_Blinding_Lights_67509023.mp3', 'path': '/static/The_Weeknd_-_Blinding_Lights_67509023.mp3', 'image': '/static/bd40e40dc8f0e5638c17b42ac3bcdff0_oKZT3gi.jpg', 'author': 'the weeknd'},
                  {'title': 'Save_Your_Tears', 'audio_path': '/static/The_Weeknd_-_Save_Your_Tears_68853145.mp3', 'path': '/static/The_Weeknd_-_Save_Your_Tears_68853145.mp3', 'image': '/static/bd40e40dc8f0e5638c17b42ac3bcdff0_oKZT3gi.jpg', 'author': 'the weeknd'},
                  {'title': 'the hills', 'audio_path': '/static/The_Weeknd_-_The_Hills_47966148.mp3', 'path': '/static/The_Weeknd_-_The_Hills_47966148.mp3', 'image': '/static/bd40e40dc8f0e5638c17b42ac3bcdff0_oKZT3gi.jpg', 'author': 'the weeknd'},
                  {'title': 'starboy', 'audio_path': '/static/The_Weeknd_Daft_Punk_-_Starboy_47829067.mp3', 'path': '/static/The_Weeknd_Daft_Punk_-_Starboy_47829067.mp3', 'image': '/static/bd40e40dc8f0e5638c17b42ac3bcdff0_oKZT3gi.jpg', 'author': 'the weeknd'}]

    return JsonResponse({"json_list": track_list})


def tracks(request):
    current_user = request.user
    # if request.method == "POST":
    #     current_user = request.user
    #     current_playlist = Playlist.objects.get(user=current_user, name='favorite')
    #
    #     current_playlist_data = {
    #         'name': current_playlist.name,
    #         'tracks': [],
    #     }
    #
    #     for track in current_playlist.tracks.all():
    #         track_data = {
    #             'title': track.name,
    #             'audio_path': track.location,
    #         }
    #
    #         current_playlist_data['tracks'].append(track_data)
    #     # print(current_playlist_data)
    #     return JsonResponse(current_playlist_data, content_type='application/json')
    #
    playlist = Playlist.objects.get(user=current_user, name='favorite')

    return render(request, 'app/user_music.html', {'playlist': playlist})

    # return render(request, 'app/user_music.html')

"""если play то с ajax как то и чтобы id отправлялся а если список треков то просто выводится но наверное получается также по нажатию"""
def playlists(request):
    #
    # """когда страница загружается вызывается в мини плеер favorite плейлист пользователя"""
    current_user = request.user
    #
    # if request.method == "POST":
    #     if "django_play_button" in request.POST:
    #         playlist_id = request.POST.get('play-button')
    #         current_playlist = UserMusic.objects.get(user=current_user, id=playlist_id)
    #
    #         current_playlist_data = {
    #             'name': current_playlist.playlist.name,
    #             'tracks': [],
    #         }
    #
    #         for track in current_playlist.playlist.tracks.all():
    #             track_data = {
    #                 'title': track.name,
    #                 'audio_path': track.location,
    #                 'image': track.image,
    #             }
    #
    #             current_playlist_data['tracks'].append(track_data)
    #
    #         return JsonResponse(current_playlist_data, content_type='application/json')
    #
    #     if "django_playlist_tracks_button" in request.POST:
    #         playlist_id = request.POST.get('play-button')
    #         return redirect('playlist', id=playlist_id)
    #
    #
    list_playlists = UserMusic.objects.filter(user=current_user)
    favorite_playlist = Playlist.objects.get(user=current_user, name='favorite')
    favorite_playlist_id = UserMusic.objects.get(user=current_user, playlist=favorite_playlist)
    #
    return render(request, 'app/user_playlists.html', {'favorite_id': favorite_playlist_id, 'playlists': list_playlists})
    # return render(request, 'app/user_playlists.html')


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
