from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.db.models import Prefetch
from django.http import FileResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
import json
from .models import TrackList, CustomUser, UserMusic, Playlist, PlaylistTracks
from .forms import SignUpForm, AuthenticationForm, LoginForm, TrackListForm
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse, HttpResponse


def signup(request):
    if request.user.is_authenticated:
        return redirect('/homepage')
    else:
        if request.method == 'POST':
            form = SignUpForm(request.POST)
            if form.is_valid():
                user = form.save()
                playlist = Playlist.objects.create(name='favorite', user=user)
                UserMusic.objects.create(user=user, playlist=playlist)
                login(request, user)

                return redirect('/homepage')

        else:
            form = SignUpForm()

    return render(request, 'app/signup.html', {'form': form})


def log_in(request):
    if request.user.is_authenticated:
        return redirect('/homepage')
    else:
        if request.method == 'POST':
            form = LoginForm(data=request.POST)
            if form.is_valid() and form.clean():
                email = form.cleaned_data['username']
                user = CustomUser.objects.get(email=email)
                remember_me = request.POST.get('remember-me')
                if not remember_me:
                    request.session.set_expiry(0)
                    request.session.modified = True
                if user is not None:
                    login(request, user)
                    return redirect('/homepage')
        else:
            form = LoginForm()

    return render(request, 'app/login.html', {'form': form})


"""главная страница где по умолчанию плейлист favorite для пользователя"""
def index(request):
    print(request.user.is_active)
    return render(request, 'app/homepage.html')


"""выбор плейлиста по нажатию по id"""
def select_playlist(request):
    current_user = request.user
    playlist_id = request.GET.get('id')
    favorite_playlist = Playlist.objects.get(user=current_user, name='favorite')
    list_of_favorite_tracks = []
    for track in favorite_playlist.tracks.all():
        list_of_favorite_tracks.append(track.id)
    # using favorite playlist id if None.
    if playlist_id is None:  # if playlist is not saved in local, function in js send None instead playlist_id.
        playlist_id = favorite_playlist.id

    current_playlist = UserMusic.objects.get(user=current_user, playlist_id=playlist_id)
    current_playlist_data = {
        'playlist_id': current_playlist.playlist.id,
        'favorite_playlist': favorite_playlist.id,
        'name': current_playlist.playlist.name,
        'tracks': [],
    }

    for track in current_playlist.playlist.tracks.all():
        default_status_value = False  # if track isn't adding in favorite playlist.
        if track.id in list_of_favorite_tracks:  # if track is adding in favorite playlist.
            default_status_value = True
        # playlists where track are.
        playlist_by_track_id = Playlist.objects.values_list('id', flat=True).filter(tracks=track.id)
        track_data = {
            'id': track.id,
            'title': track.name,
            'path': track.location,
            'image': track.image,
            'author': track.author,
            'status': default_status_value,
            'playlists_for_track': list(playlist_by_track_id)
        }

        current_playlist_data['tracks'].append(track_data)

    return JsonResponse(current_playlist_data)


def add_track_to_playlist(request):  # function for adding a track to the playlist.
    ...
    current_user = request.user
    track_id = request.GET.get('track_id')
    track = TrackList.objects.get(id=track_id)
    playlist_id = request.GET.get('playlist_id')
    playlist = Playlist.objects.get(id=playlist_id)
    if playlist.user == current_user:
        playlist.tracks.add(track)
        playlist.save()
    return HttpResponse()


def delete_track(request):  # function for deleting a track from playlist.
    ...
    current_user = request.user
    track_id = request.GET.get('track_id')
    track = TrackList.objects.get(id=track_id)
    playlist_id = request.GET.get('playlist_id')
    playlist = Playlist.objects.get(id=playlist_id)
    if playlist.user == current_user:
        playlist.tracks.remove(track)
    return HttpResponse()


@login_required(login_url='/login')
def tracks(request):
    current_user = request.user
    playlist = Playlist.objects.get(user=current_user, name='favorite')

    return render(request, 'app/user_music.html', {'playlist': playlist})


@login_required(login_url='/login')
def playlists(request):
    current_user = request.user
    list_playlists = UserMusic.objects.filter(user=current_user)

    return render(request, 'app/user_playlists.html', {'playlists': list_playlists})


# add playlist to user library.
def playlist_add_to_user(request):
    ...
    current_user = request.user
    user = CustomUser.objects.get(id=current_user.id)
    playlist_id = request.GET.get('playlist_id')
    playlist = Playlist.objects.get(id=playlist_id)
    user.any_playlist.add(playlist)
    return HttpResponse()


# delete playlist only from user library.
def playlist_delete_from_user(request):
    ...
    current_user = request.user
    user = CustomUser.objects.get(id=current_user.id)
    playlist_id = request.GET.get('playlist_id')
    playlist = Playlist.objects.get(id=playlist_id)
    user.any_playlist.remove(playlist)
    return HttpResponse()


"""if you need to make the function that will work in other pages, implement it using onClick and ajax,
send playlist id to django from js"""


def playlist_tracks(request, id):  # function to show all tracks in selected playlist.
    current_user = request.user
    playlist_status = False
    # current_user = CustomUser.objects.get(id=curr_user.id).
    playlist = Playlist.objects.get(id=id)
    if UserMusic.objects.filter(user=current_user, playlist=playlist).exists():  # check if object exist in db.
        playlist_status = True
    if request.method == 'POST':
        # for delete a playlist (full deleting from db).
        if 'del_button' in request.POST and playlist.user == current_user:  # delete button on page where playlist tracks.
            curr_playlist = UserMusic.objects.get(user=current_user, playlist=playlist)
            curr_playlist.delete()
            playlist.delete()
        if 'edit_button' in request.POST and playlist.user == current_user:
            return redirect(f'/edit_playlist/{id}/')
        
        return redirect('/playlists')
    return render(request, 'app/user_music.html', {'playlist': playlist, 'playlist_status': playlist_status})


def edit_playlist(request, id):
    current_user = request.user
    # plalist_status = False (?)
    playlist = Playlist.objects.get(id=id)
    playlist_info = PlaylistTracks.objects.filter(playlist=id)
    tracks_dict = {i.order_id: i.track for i in playlist_info}
    if request.method == 'POST':
        order_ids = request.POST.getlist('orderIds[]')
        print(order_ids)

        list_of_track_ids = []

        for i in order_ids:
            track_info = PlaylistTracks.objects.get(order_id=int(i))
            list_of_track_ids.append(track_info.track.id)
        counter = 1
        for i in list_of_track_ids:
            track = TrackList.objects.get(id=i)
            track_info = PlaylistTracks.objects.get(order_id=counter)
            track_info.track = track
            track_info.save()
            counter += 1

        # ordered_track_names = [tracks_dict[int(order_id)] for order_id in order_ids]
        # for i in range(len(ordered_track_names)):
        #     pltr = PlaylistTracks.objects.get(order_id=i+1)
        #     track = TrackList.objects.get(id=pltr.track.id)
        #     print(track)
    # for i in playlist_info:
        # print(i.track, i.order_id)
    return render(request, 'app/edit_playlist.html', {'playlist': playlist, 'playlist_info': playlist_info})


def track_all_playlists(request):
    ...
    current_user = request.user
    track_id = request.GET.get('track_id')

    track_playlist_list = []
    data_playlists_list = []

    track_playlists = Playlist.objects.filter(tracks=track_id)
    for playlist in track_playlists:
        track_playlist_list.append(playlist.id)
    user_playlists = Playlist.objects.filter(user=current_user)
    for playlist in user_playlists:
        playlist_status = False
        if playlist.id in track_playlist_list:
            playlist_status = True
        playlist_info = {
            'playlist_id': playlist.id,
            'playlist_name': playlist.name,
            'playlist_status': playlist_status
        }
        data_playlists_list.append(playlist_info)

    return JsonResponse({'playlist': data_playlists_list})


def top_playlists(request):
    pass


@login_required(login_url='/login')
def create_playlist(request):
    ...
    current_user = request.user
    favorite_playlist = Playlist.objects.get(user=current_user, name='favorite')
    if request.method == "POST":
        playlist_name = request.POST.get('name_of_playlist')
        playlist_description = request.POST.get('description_of_playlist')
        playlist_image = None
        track_list = request.POST.getlist('checks')
        if playlist_name != '':
            new_playlist = Playlist.objects.create(user=current_user, name=playlist_name, about=playlist_description)
            if len(track_list) != 0:
                for track in track_list:
                    add_track = TrackList.objects.get(id=int(track))
                    new_playlist.tracks.add(add_track)
            new_playlist.save()
            UserMusic.objects.create(user=current_user, playlist=new_playlist)
            return redirect('/homepage')
    return render(request, 'app/create_playlist.html', {'favorite_playlist': favorite_playlist})


@login_required(login_url='/login')
def load_track(request):
    current_user = request.user
    if request.method == "POST":
        form = TrackListForm(request.POST, request.FILES)
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
