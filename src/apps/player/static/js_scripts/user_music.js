const imageContainer = document.querySelector('.image-container');
	const playImg = document.querySelector('#play-img');

	imageContainer.addEventListener('mouseover', function() {
	  playImg.style.opacity = 1;
	});

	imageContainer.addEventListener('mouseout', function() {
	  playImg.style.opacity = 0;
	});

function addDelPlaylistToUser(playlistId, playlistStatus) {
    var url = (playlistStatus == 'True') ? '/playlist_delete_from_user/' : '/playlist_add_to_user/';
    $.ajax({
        url: url,
        type: 'GET',
        data: {
          'csrfmiddlewaretoken': $('[name="csrfmiddlewaretoken"]').val(),
          'playlist_id': playlistId
        },
        success: function(){
        }
    })
}

