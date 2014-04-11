$(function() {

	/* POPUPS */

        openLoginPopup = function(){
                $('#popup-login').lightbox_me({
                centered: true,
                onLoad: function() {
                },
                closeSelector: '.close-popup',
        });
        }

        $('.login-button').click(function(e){
                openLoginPopup();
        });
	openRegisterPopup = function(){
		$('#popup-register').lightbox_me({
	        centered: true,
	        onLoad: function() {
	        },
	        closeSelector: '.close-popup',
        });
	}

	$('#register-button').click(function(e){
		openRegisterPopup();
	});

});