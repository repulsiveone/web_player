// тут выбраны все элементы на html странице и присвоены переменным
let track_art = document.querySelector(".track-art");
let track_name = document.querySelector(".player-track-name");
let track_artist = document.querySelector(".track-artist");
let main_play_btn = document.querySelector(".main-button");

let playpause_btn = document.querySelector(".playpause-track");
let adddel_btn = document.querySelector(".add-track");
let next_btn = document.querySelector(".next-track");
let prev_btn = document.querySelector(".prev-track");
let send_btn = document.querySelector(".send-id");
//let adddelplaylist_btn = document.querySelector(".add-playlist-to-user");

let data_btn = document.querySelector(".data-id");

let seek_slider = document.querySelector(".seek_slider");
let volume_slider = document.querySelector(".volume_slider");
let curr_time = document.querySelector(".current-time");
let total_duration = document.querySelector(".total-duration");

// используемые значения
let track_index = 0;
let isPlaying = false;
let updateTimer;

// аудио элемент для плеера
let curr_track = document.createElement('audio');
let containerElement = document.getElementById("container");
let track_list = []

// значения из локальной памяти браузера
var saved_playlist = JSON.parse(localStorage.getItem('playlist'));
var saved_volume = JSON.parse(localStorage.getItem('volume'));

// переменные для получения плейлистов через ajax
var current_playlist_id = null;
var favorite_playlist_id = null;

// функция для получения плейлистов с django
function getPlaylistData(playlistId) {
  event.preventDefault();
  $.ajax({
    url: '/select_playlist/', // django функция
    type: 'GET',
    data: {
      'csrfmiddlewaretoken': $('[name="csrfmiddlewaretoken"]').val(),
      'id': playlistId // отправляется id в django
    },
    success: function(response){
      // получаем все отправленные значения
      track_list = []
      current_playlist_id = response.playlist_id;
      favorite_playlist_id = response.favorite_playlist;
      response.tracks.forEach(function(tracks) {
                track_list.push({
                'id': tracks.id,
                'title': tracks.title,
                'path': tracks.path,
                'author': tracks.author,
                'image': tracks.image,
                'status': tracks.status,
                'playlists_for_track': tracks.playlists_for_track
                })
            })
      localStorage.setItem('playlist', JSON.stringify(track_list)); // сохранение в локальную память
    },
    complete: function() {
        let existingCells = document.querySelectorAll('.cell');

        // удаляется каждый элемент
        existingCells.forEach(cell => {
          cell.remove();
        });
        // создание элементов для правого выдвигающегося окна с данными о новом плейлисте
        for (let i = 0; i < track_list.length; i++) {
                let cellElement = document.createElement("div");
                cellElement.insertAdjacentHTML('beforeend', `
                <img src='${track_list[i].image}' alt=''>
                <div class='info'>
                <h2>${track_list[i].title}</h2>
                <p>${track_list[i].author}</p>
                </div>`);
                cellElement.classList.add("cell");
                containerElement.append(cellElement);
            }
         loadTrack(track_index);
         playpauseTrack();
         },
    error: function(xhr, status, error) {
      // обработка ошибки AJAX
      console.log(error);
    }
  });
}
// проверка локальной памяти для слайдера звука
if (saved_volume) {
    curr_track.volume = saved_volume;
}else{
}
// проверка локальной памяти на наличие плейлиста
if(saved_playlist){
  // Использовать плейлист
  track_list = saved_playlist;
  for (let i = 0; i < track_list.length; i++) {
        let cellElement = document.createElement("div");
        cellElement.insertAdjacentHTML('beforeend', `
        <img src='${track_list[i].image}' alt=''>
        <div class='info'>
        <h2>${track_list[i].title}</h2>
        <p>${track_list[i].author}</p>
        </div>`);
        cellElement.classList.add("cell");
        containerElement.append(cellElement);
    }
}else{
    getPlaylistData(); // плейлист favorite если локальная память пуста
}

// функции чтобы менялась только часть content в html и для работы навигации, нужны для того чтобы играла музыка на всех
// страницах, используя html шаблон
$(document).ready(function() {
  function loadContent(url) {
  $('#content').load(url + ' #content > *');
}

  function changePage(url) {
    window.history.pushState(null, null, url);
    loadContent(url);
  }

  // Навигация по ссылкам
  $(document).on('click', 'a', function(e) {
    e.preventDefault();
    var url = $(this).attr('href');
    changePage(url);
  });

  // Инициализация при первой загрузке страницы
  loadContent(window.location.href);
});

// tracks
function playcurrTrack(location) {
    event.preventDefault();
    console.log(location);
    const trackIndex = getTrackIndexByPath(location);
    loadTrack(trackIndex);
    playTrack();
}
// tracks
function getTrackIndexByPath(path) {
  const index = track_list.findIndex(item => item.path === path);
  return index;
}

// кнопки на самих треках
function loadTrack(track_index) {
// обнуляет ползунок после предыдущего трека
clearInterval(updateTimer);
resetValues();
}
// лоадит новый трек
curr_track.src = track_list[track_index].path;
curr_track.load();

// апдейтит дательки трека
track_art.style.backgroundImage =
	"url(" + track_list[track_index].image + ")";
track_name.textContent = track_list[track_index].title;
track_artist.textContent = track_list[track_index].author;

// интервал в 1000 миллисекунд для обновления ползунка
updateTimer = setInterval(seekUpdate, 1000);

// Переход к следующему треку, если текущий закончил воспроизведение
curr_track.addEventListener("ended", nextTrack);

// Функция для сброса всех значений по умолчанию
function resetValues() {
curr_time.textContent = "00:00";
total_duration.textContent = "00:00";
seek_slider.value = 0;
}


function loadTrack(track_index) {
    // Очистить предыдущий таймер трека
    clearInterval(updateTimer);
    resetValues();

//     лоадит новый трек х2
    curr_track.src = track_list[track_index].path;
    curr_track.load();

//     Обновляет инфу о треке
    track_art.style.backgroundImage =
        "url(" + track_list[track_index].image + ")";
    track_name.textContent = track_list[track_index].title;
    track_artist.textContent = track_list[track_index].author;

    //интервал в 1000 миллисекунд для обновления бегунка поиска
    updateTimer = setInterval(seekUpdate, 1000);

    // переход к следующему треку если текущий закончил воспроизведение
    curr_track.addEventListener("ended", nextTrack);
    }

    // Функция для сброса всех значений по умолчанию
    function resetValues() {
    curr_time.textContent = "00:00";
    total_duration.textContent = "00:00";
    seek_slider.value = 0;
    }

    function playpauseTrack() {
        addDelIconChange();
        // Переключение между воспроизведением и паузой в зависимости от текущего состояния
        if (!isPlaying) playTrack();
        else pauseTrack();
        }

        function playTrack() {
        // Воспроизвести загруженный трек
        curr_track.play();
        isPlaying = true;

        // замена значка на значок паузы
        playpause_btn.innerHTML = '<i class="fa fa-pause-circle fa-5x"></i>';
        }

        function pauseTrack() {
        // пауз трек
        curr_track.pause();
        isPlaying = false;

        // замена значка на значок воспроизведения
        playpause_btn.innerHTML = '<i class="fa fa-play-circle fa-5x"></i>';
        }

        function nextTrack() {
        addDelIconChange();
//        вернуться к первому треку если это последний трек
        if (track_index < track_list.length - 1)
            track_index += 1;
        else track_index = 0;
//         загрузить и запустить новый трек
        loadTrack(track_index);
        playTrack();
        }

        function prevTrack() {
        addDelIconChange();
//         Вернуться к последней дорожке если текущий стоит первым в списке треков
        if (track_index > 0)
            track_index -= 1;
        else track_index = track_list.length - 1;

//         загрузить и запустить новый трек
        loadTrack(track_index);
        playTrack();
        }
//// функция для замены кнопки добавить плейлист в библиотеку
//    function addDelPlaylistIconChange(status_of_playlist) {
//        id (status_of_playlist === false) adddelplaylist_btn.innerHTML = '<i class="fa fa-plus" aria-hidden="true"></i>';
//        else adddelplaylist_btn.innerHTML = '<i class="fa fa-times" aria-hidden="true"></i>';
//    }
//
//    function addDelPlaylistToUser() {
//
//    }

// функция для замены кнопки добавить трек
    function addDelIconChange() {
        console.log(track_list[track_index].status);
        if (track_list[track_index].status == true) adddel_btn.innerHTML = '<i class="fa fa-heart" aria-hidden="true"></i>';
        else adddel_btn.innerHTML = '<i class="far fa-heart" aria-hidden="true"></i>';
    }
    // для favorite, добавление или удаление выбранного трека из плейлиста favorite
    function addDelTrack() {
    console.log(track_list[track_index].status, track_list[track_index].id);
    var url = (track_list[track_index].status == true) ? '/delete_track/': '/add_track_to_playlist/';
    console.log(url)
        $.ajax({
            url: url,
            type: 'GET',
            data: {
              'csrfmiddlewaretoken': $('[name="csrfmiddlewaretoken"]').val(),
              'track_id': track_list[track_index].id,
              'playlist_id': favorite_playlist_id
            },
            success: function(){
                getPlaylistData(current_playlist_id); // обновляет текущий плейлист
            }
        })
    }

    function playlistsList() {
        $(".block_with_playlists").fadeToggle(100); // появелние элемента
        $.ajax({
            url: '/track_all_playlists/',  // получаем все плейлисты пользователя в которых есть выбранный трек
            type: 'GET',
            data: {
              'csrfmiddlewaretoken': $('[name="csrfmiddlewaretoken"]').val(),
              'track_id': track_list[track_index].id
            },
            success: function(response){ // создает окно с плейлистами пользователя
                var isWhiteSquareCreated = false;
                if (!isWhiteSquareCreated) {
                    var whiteSquare = document.createElement('div');
                    whiteSquare.className = 'block_with_playlists';
                    for (let i = 0; i < response.playlist.length; i++) {
                    console.log(response.playlist[i].playlist_status);
                    whiteSquare.insertAdjacentHTML('beforeend',
                    `<div class="playlist_view">
                    <div style="display: inline-block;" class="add_to_playlist" onclick="addDelToPlaylist('${response.playlist[i].playlist_status}', '${response.playlist[i].playlist_id}')">
                        ${response.playlist[i].playlist_status ? '<i class="fa fa-check" aria-hidden="true"></i>' : '<i class="fa fa-plus" aria-hidden="true"></i>'}
                    </div>
                    <h2 style="display: inline-block;">${response.playlist[i].playlist_name}</h2>
                    </div>`
                    );}
                    whiteSquare.classList.add("playlistik");
                    document.body.append(whiteSquare);
                    isWhiteSquareCreated = true;
                }
            }
        })
    }

$(document).mouseup(function (e) {
    var container = $(".block_with_playlists");
    if (container.has(e.target).length === 0){
        container.hide();
    }
});

    function addDelToPlaylist(playlistStatus, playlistId) {
        console.log('meow');
        console.log(playlistStatus);
        var url = (playlistStatus == 'true') ? '/delete_track/' : '/add_track_to_playlist/';
        console.log(url);
        $.ajax({
            url: url,
            type: 'GET',
            data: {
            'csrfmiddlewaretoken': $('[name="csrfmiddlewaretoken"]').val(),
              'track_id': track_list[track_index].id, // берется текущий трек, чтобы функция работала с других страниц, нужно как-то передавать id в onclick функцию
              'playlist_id': playlistId,
            },
            success: function(response){
            }
        })
    }

        function seekTo() {
            // расчитывает позицию поиска по проценту ползунка поиска
             // = относительная длительность трека
            seekto = curr_track.duration * (seek_slider.value / 100);

            // устанавливает текущую позицию трека на рассчитанную позицию ползунка
            curr_track.currentTime = seekto;
            }

            function setVolume() {
            // установка громкости в соответствии с
             // процентом установленного ползунка громкости
            curr_track.volume = volume_slider.value / 100;
            localStorage.setItem('volume', JSON.stringify(volume_slider.value / 100));
            }

            function seekUpdate() {
            let seekPosition = 0;

            // Проверяем, является ли продолжительность текущей дорожки разборчивым числом
            if (!isNaN(curr_track.duration)) {
                seekPosition = curr_track.currentTime * (100 / curr_track.duration);
                seek_slider.value = seekPosition;

                // расчитывает оставшееся время и общую продолжительность
                let currentMinutes = Math.floor(curr_track.currentTime / 60);
                let currentSeconds = Math.floor(curr_track.currentTime - currentMinutes * 60);
                let durationMinutes = Math.floor(curr_track.duration / 60);
                let durationSeconds = Math.floor(curr_track.duration - durationMinutes * 60);

                // добавляет ноль к значениям времени
                if (currentSeconds < 10) { currentSeconds = "0" + currentSeconds; }
                if (durationSeconds < 10) { durationSeconds = "0" + durationSeconds; }
                if (currentMinutes < 10) { currentMinutes = "0" + currentMinutes; }
                if (durationMinutes < 10) { durationMinutes = "0" + durationMinutes; }

                // показывает обновленную продолжительность трека
                curr_time.textContent = currentMinutes + ":" + currentSeconds;
                total_duration.textContent = durationMinutes + ":" + durationSeconds;
            }
            }

            // загружает первый трек в списке треков
loadTrack(track_index);
