from django.http import FileResponse
from django.shortcuts import render, redirect
from django.contrib import auth
import json
from .models import TrackList, CustomUser, UserMusic
from .forms import SignUpForm, LoginForm


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


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            """hash for password"""
            user = CustomUser.objects.get(email=form.cleaned_data.get('email'), password=form.cleaned_data.get('password'))
            if user is not None:
                auth.login(request, user)
                return redirect('/homepage')
            else:
                """alert"""
                pass
    else:
        form = LoginForm()

    return render(request, 'app/login.html', {'form': form})


def index(request):
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


def new_releases(request):
    pass


def chart(request):
    pass


def playlists(request):
    pass


def tracks(request):
    pass


def history(request):
    pass


def chats(request):
    pass


def userpage(request):
    pass


def setting(request):
    pass
