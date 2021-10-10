function remove() {
	var type = this.parentElement.id
	$.post('/remove', {'id': this.id, 'type': type
	}).done(function() {
		location.reload(true)
	}).fail(function() {});
}

var removeButtons = document.querySelectorAll('.removeButton');
var i;
for (i=0; i<removeButtons.length; i++) {
	removeButtons[i].addEventListener('click', remove);
}