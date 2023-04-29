from django.http import FileResponse
from django.shortcuts import render
import json


""" main page with player """
# def index(request):

    # return render(request, 'app/index.html')


"""1: вывод плейлиста из базы в список и отправка в джс
   2: id += 1 и отправка в функцию джанго и вызов с бд
   можно сделать разные id для треков и отдельные id в плейлистах для корректного вывода"""


def index(request):
    data = [{'path': '/static/принц.mp3', 'image': '/static/китик.jpg'}, {'path': '/static/mana_break.mp3', 'image': '/static/китик.jpg'}]
    # geodata = [("Here", (1003, 3004)), ("There", (1.2, 1.3))]

    # data = '/static/принц.mp3'
    # for i in data:
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
