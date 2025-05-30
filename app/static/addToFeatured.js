function addToFeatured() {
	$.post('/add_to_featured', {id: this.id
	}).done(function(response) {
		alert(response['message'])
	}).fail(function() {
		alert('Unable to add to featured')
	});
}

var addButtons = document.querySelectorAll('.addButton');
var i;
for (i=0; i<addButtons.length; i++) {
	addButtons[i].addEventListener('click', addToFeatured);
}