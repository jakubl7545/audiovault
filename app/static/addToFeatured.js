function addToFeatured() {
	$.post('/add_to_featured', {id: this.id
	}).done(function() {
		location.reload(true)
	}).fail(function() {});
}

for (let addButton of document.querySelectorAll('.addButton')) {
	addButton.addEventListener('click', addToFeatured);
}
