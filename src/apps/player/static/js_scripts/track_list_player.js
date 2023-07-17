const playButtons = document.getElementsByClassName('play-button');
let curr_track = document.createElement('audio');

function playTrack(location) {
    curr_track.src = location;
    curr_track.load();
    curr_track.play();
}

function playButtonClick(event) {
    event.preventDefault();
    const location = event.target.dataset.location;
    playTrack(location);
}

for (let i = 0; i < playButtons.length; i++) {
    playButtons[i].addEventListener('click', playButtonClick);
}
