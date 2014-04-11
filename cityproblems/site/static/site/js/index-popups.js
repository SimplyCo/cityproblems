$(function() {

	/* POPUPS */

	openFilterCategoryPopup = function(){
		$('#popup-filter-category').lightbox_me({
	        centered: true,
	        onLoad: function() {
	        },
	        closeSelector: '.close-popup',
        });
	}

	$('#filter-category-button').click(function(e){
		openFilterCategoryPopup();
	});


});