from django.http import FileResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login
import json
from .models import TrackList, CustomUser, UserMusic, Playlist
from .forms import SignUpForm, AuthenticationForm, LoginForm
from django.contrib.auth.hashers import check_password


""" main page with player """
# def index(request):

    # return render(request, 'app/index.html')


"""1: вывод плейлиста из базы в список и отправка в джс
   2: id += 1 и отправка в функцию джанго и вызов с бд
   можно сделать разные id для треков и отдельные id в плейлистах для корректного вывода"""


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        """best way make func in form"""
        if form.is_valid():
            form.save()
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


def index(request):
    print(request.user.email)
    if request.method == 'POST':
        id_of_track = request.POST.get('id')
        current_track = TrackList.objects.get(id=id_of_track)
        current_user = request.user
        user = CustomUser.objects.get(id=current_user.id)
        if user.track.filter(id=id_of_track).exists():
            """alert on page that track has already added in bd / or change button"""
            pass
        else:
            user.track.add(current_track)
            user.save()

    data = []
    base = TrackList.objects.all()
    for item in base:
        data.append({'id': item.id, 'path': item.location, 'image': '/static/китик.jpg', 'name': item.name})

    return render(request, 'app/player.html', {'data': json.dumps(data)})


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
