function generate() {
	var title = document.getElementById('name');
	var description = document.getElementById('description');
	fetch('/generate_description', {method: 'POST',
		headers: {'Content-Type': 'application/x-www-form-urlencoded'},
		body: `title=${encodeURIComponent(title.value)}`
	}).then(response => {return response.json();
		}).then(data => {description.value += `${data.description}`;
	}).catch(error => {});
}

var generateButton = document.querySelector('#generate_description');
generateButton.addEventListener('click', generate);
