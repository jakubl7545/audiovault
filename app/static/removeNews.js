function removeNews() {
	fetch('/remove_news', {method: 'POST',
		headers: {'Content-Type': 'application/x-www-form-urlencoded'},
		body: `id=${encodeURIComponent(this.id)}`
	}).then(response => {
		location.reload(true)
	}).catch(error => {});
}

for (let removeButton of document.querySelectorAll('.removeNewsButton')) {
	removeButton.addEventListener('click', removeNews);
}
