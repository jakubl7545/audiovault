function removeFeatured() {
	$.post('/remove_featured', {'id': this.id
	}).done(function() {
		location.reload(true)
	}).fail(function() {});
}

for (let removeButton of document.querySelectorAll('.removeFeaturedButton')) {
	removeButton.addEventListener('click', removeFeatured);
}
