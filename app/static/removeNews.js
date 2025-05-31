function removeNews() {
	$.post('/remove_news', {'id': this.id
	}).done(function() {
		location.reload(true)
	}).fail(function() {});
}

for (let removeButton of document.querySelectorAll('.removeNewsButton')) {
	removeButton.addEventListener('click', removeNews);
}
