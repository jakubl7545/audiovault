function clearFeatured() {
	fetch('/clear_featured', {method: 'POST',
		headers: {'Content-Type': 'application/x-www-form-urlencoded'}
	}).then(response => {
		location.reload(true)
	}).catch(error => {});
}

var clearButton = document.querySelector('#clear_featured');
if (clearButton !== null) {
	clearButton.addEventListener('click', clearFeatured);
}
