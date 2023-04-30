from django.http import FileResponse
from django.shortcuts import render
import json
from .models import TrackList


""" main page with player """
# def index(request):

    # return render(request, 'app/index.html')


"""1: вывод плейлиста из базы в список и отправка в джс
   2: id += 1 и отправка в функцию джанго и вызов с бд
   можно сделать разные id для треков и отдельные id в плейлистах для корректного вывода"""


def index(request):
    data = []
    bd = TrackList.objects.all()
    for i in bd:
        data.append({'path': i.location, 'image': '/static/китик.jpg'})

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
