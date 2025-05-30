function removeFeatured() {
	$.post('/remove_featured', {'id': this.id
	}).done(function() {
		location.reload(true)
	}).fail(function() {});
}

var removeButtons = document.querySelectorAll('.removeFeaturedButton');
var i;
for (i=0; i<removeButtons.length; i++) {
	removeButtons[i].addEventListener('click', removeFeatured);
}