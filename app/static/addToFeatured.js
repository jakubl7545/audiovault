function addToFeatured() {
	$.post('/add_to_featured', {id: this.id
	}).done(function(response) {
		alert(response['message'])
	}).fail(function() {
		alert('Unable to add to featured')
	});
}

for (let addButton of document.querySelectorAll('.addButton')) {
	addButton.addEventListener('click', addToFeatured);
}