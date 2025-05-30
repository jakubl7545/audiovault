function removeNews() {
	$.post('/remove_news', {'id': this.id
	}).done(function() {
		location.reload(true)
	}).fail(function() {});
}

var removeButtons = document.querySelectorAll('.removeNewsButton');
var i;
for (i=0; i<removeButtons.length; i++) {
	removeButtons[i].addEventListener('click', removeNews);
}