const imageContainer = document.querySelector('.image-container');
	const playImg = document.querySelector('#play-img');

	imageContainer.addEventListener('mouseover', function() {
	  playImg.style.opacity = 1;
	});

	imageContainer.addEventListener('mouseout', function() {
	  playImg.style.opacity = 0;
	});
