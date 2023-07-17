let play_btn = document.querySelector(".play-button");
let curr_track = document.createElement('audio');

//let track_list = []
window.onload = load()
//// по открытию страницы выполняется функция загрузки данных из бд
function load() {
//    event.preventDefault();
    $.ajax({
        url: "tracks/",
        type: "POST",
        dataType: 'json',
        data: {
        'csrfmiddlewaretoken': $('[name="csrfmiddlewaretoken"]').val()
        },
//
        success: function(data) {
            console.log(data)
        }
//            data.tracks.forEach(function(tracks) {
//                track_list.push({
//                'id': '1',
//                'name': tracks.title,
//                'path': tracks.audio_path,
//                'artist': "zxcursed",
//                'image': "/static/китик.jpg"
//                })
//            })
//        },
//
////        complete: function() {
////                loadTrack(track_index);
////                }
    });
}

//curr_track.src = track_list[track_index].path;
//curr_track.load();
function playTrack(location) {
    curr_track.src = location;
    curr_track.load();
    curr_track.play();
}