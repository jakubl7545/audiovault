function removeFeatured() {
	fetch('/remove_featured', {method: 'POST',
		headers: {'Content-Type': 'application/x-www-form-urlencoded'},
		body: `id=${encodeURIComponent(this.id)}`
	}).then(response => {
		location.reload(true);
	}).catch(error => {});
}

for (let removeButton of document.querySelectorAll('.removeFeaturedButton')) {
	removeButton.addEventListener('click', removeFeatured);
}
