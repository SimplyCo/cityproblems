$(function() {

	/* POPUPS */

	openLoginPopup = function(){
		$('#popup-login').lightbox_me({
	        centered: true,
	        onLoad: function() {
	        },
	        closeSelector: '.closePopup',
        });
	}

	$('.login-button').click(function(e){
		openLoginPopup();
	});


});