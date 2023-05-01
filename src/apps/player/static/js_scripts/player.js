// тут выбраны все элементы на хтмл странице и присвоены переменным
let now_playing = document.querySelector(".now-playing");
let track_art = document.querySelector(".track-art");
let track_name = document.querySelector(".track-name");
let track_artist = document.querySelector(".track-artist");

let test_data = JSON.parse(document.getElementById('test').textContent);

let playpause_btn = document.querySelector(".playpause-track");
let next_btn = document.querySelector(".next-track");
let prev_btn = document.querySelector(".prev-track");
let send_btn = document.querySelector(".send-id")

let seek_slider = document.querySelector(".seek_slider");
let volume_slider = document.querySelector(".volume_slider");
let curr_time = document.querySelector(".current-time");
let total_duration = document.querySelector(".total-duration");

// используемые знаения
let track_index = 0;
let isPlaying = false;
let updateTimer;

// аудио элемент для плеера
let curr_track = document.createElement('audio');

// трек лист
let track_list =
{
    id: test_data[track_index].id,
	name: test_data[track_index].name,
	artist: "zxcursed",
	image: test_data[track_index].image,
	path: test_data[track_index].path
}

function loadTrack(track_index) {
// обнуляет ползунок после предыдущего трека
clearInterval(updateTimer);
resetValues();
}
// лоадит новый трек
curr_track.src = test_data[track_index].path;
curr_track.load();

// апдейтит дательки трека
track_art.style.backgroundImage =
	"url(" + test_data[track_index].image + ")";
track_name.textContent = test_data[track_index].name;
track_artist.textContent = test_data[track_index].artist;
now_playing.textContent =
	"PLAYING " + (track_index + 1) + " OF " + test_data.length;

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

    // лоадит новый трек х2
    curr_track.src = test_data[track_index].path;
    curr_track.load();

    // Обновляет инфу о треке
    track_art.style.backgroundImage =
        "url(" + test_data[track_index].image + ")";
    track_name.textContent = test_data[track_index].name;
    track_artist.textContent = test_data[track_index].artist;
    now_playing.textContent =
        "PLAYING " + (track_index + 1) + " OF " + test_data.length;

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
       // вернуться к первому треку если это последний трек
        if (track_index < test_data.length - 1)
            track_index += 1;
        else track_index = 0;

        // загрузить и запустить новый трек
        loadTrack(track_index);
        playTrack();
        }

        function prevTrack() {
        // Вернуться к последней дорожке если текущий стоит первым в списке треков
        if (track_index > 0)
            track_index -= 1;
        else track_index = test_data.length - 1;

        // загрузить и запустить новый трек
        loadTrack(track_index);
        playTrack();
        }

        function favorite() {
        var id_data = test_data[track_index].id;
        $.ajax({
            url: "homepage/",
            type: "POST",
            data: {
            id: id_data,
            'csrfmiddlewaretoken': $('[name="csrfmiddlewaretoken"]').val()
            },

            success: function(json) {
                alert("мяу");
            }
        });
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
