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
    current_user = request.user
    """получить пользователя, запрос к плейлистам по id пользователю и по названию favorite, это будет current playlist"""
    """работает"""
    current_playlist = Playlist.objects.get(user=current_user, name='favorite')

    return render(request, 'app/homepage.html', {'current_playlist': current_playlist})



"""выбор плейлиста по нажатию по id"""
def select_playlist(request):
    """get потому что с ajax передаю??"""
    if request.method == "POST":
        current_playlist_id = request.POST.get('playlist_id')
        current_playlist = Playlist.objects.get(id=current_playlist_id)

        data = {'current_playlist': current_playlist}

        return JsonResponse(data)


"""возможно стоит передавать сразу плейлист"""
def update_playlist(playlist_id):
    current_playlist = Playlist.objects.get(id=playlist_id)

    data = {'current_playlist': current_playlist}

    return JsonResponse(data)


def add_track(request):
    if request.method == "POST":
        track_id = request.POST.get('track_id')
        track = TrackList.objects.get(id=track_id)
        playlist_id = request.POST.get('playlist_id')
        playlist = Playlist.objects.get(id=playlist_id)
        playlist.tracks.add(track)
        playlist.save()
        update_playlist(playlist_id)


def delete_track(request):
    if request.method == "POST":
        track_id = request.POST.get('track_id')
        track = TrackList.objects.get(id=track_id)
        playlist_id = request.POST.get('playlist_id')
        playlist = Playlist.objects.get(id=playlist_id)
        playlist.tracks.remove(track)
        playlist.save()
        update_playlist(playlist_id)


# def index(request):
#     print(request.user.email)
#     if request.method == 'POST':
#         id_of_track = request.POST.get('id')
#         current_track = TrackList.objects.get(id=id_of_track)
#         current_user = request.user
#         user = CustomUser.objects.get(id=current_user.id)
#         if user.track.filter(id=id_of_track).exists():
#             """alert on page that track has already added in bd / or change button"""
#             pass
#         else:
#             user.track.add(current_track)
#             user.save()
#
#     data = []
#     base = TrackList.objects.all()
#     for item in base:
#         data.append({'id': item.id, 'path': item.location, 'image': '/static/китик.jpg', 'name': item.name})
#
#     return render(request, 'app/player.html', {'data': json.dumps(data)})


def tracks(request):
    current_user = request.user

    user = CustomUser.objects.get(id=current_user.id)
    all_tracks = user.track.all()
    # track_names = [track.name for track in tracks]
    # print(track_names)
    #todo make this func with js
    """function for add track in playlist from js"""
    playlist = Playlist.objects.get(id=1)
    playlist.tracks.add(1)
    if request.method == 'POST':
        data = """track_id"""
        playlist = Playlist.objects.get(id=1)
        playlist.tracks.add(data)

    return render(request, 'app/user_music.html', {'tracks': all_tracks})


def playlists(request):
    playlist = Playlist.objects.get(id=1)
    playlist_tracks = playlist.tracks.all()
    return render(request, 'app/user_playlists.html', {'playlist': playlist, 'playlist_tracks': playlist_tracks})


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
