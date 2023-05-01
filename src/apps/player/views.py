from django.http import FileResponse
from django.shortcuts import render
import json
from .models import TrackList, CustomUser


""" main page with player """
# def index(request):

    # return render(request, 'app/index.html')


"""1: вывод плейлиста из базы в список и отправка в джс
   2: id += 1 и отправка в функцию джанго и вызов с бд
   можно сделать разные id для треков и отдельные id в плейлистах для корректного вывода"""


def index(request):
    if request.method == 'POST':
        id_of_track = request.POST.get('id')
        print(id_of_track)
        # current_track = TrackList.objects.get(id=id_of_track)

        # current_user = request.user
        # track = TrackList.objects.get(name=current_track)
        # user = CustomUser.objects.get(id=current_user.id)
        # user.track.add(track)
        # user.save()

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
