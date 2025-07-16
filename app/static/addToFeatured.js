function addToFeatured() {
	fetch('/add_to_featured', {method: 'POST',
		headers: {'Content-Type': 'application/x-www-form-urlencoded'},
		body: `id=${encodeURIComponent(this.id)}`
	}).then(response => {
		location.reload(true)
	}).catch(error => {});
}

for (let addButton of document.querySelectorAll('.addButton')) {
	addButton.addEventListener('click', addToFeatured);
}
