function clearFeatured() {
	fetch('/clear_featured', {method: 'POST',
		headers: {'Content-Type': 'application/x-www-form-urlencoded'}
	}).then(response => {
		location.reload(true)
	}).catch(error => {});
}

var clearButton = document.querySelector('#clear_featured');
clearButton.addEventListener('click', clearFeatured)
