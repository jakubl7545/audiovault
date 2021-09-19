function toggleFeatured() {
	var content = this.nextElementSibling;
	if (content.style.display == "none") {
		content.style.display = "block";
		this.ariaExpanded = true;
	} else {
		content.style.display = "none";
		this.ariaExpanded = false;
	}
}
var buttons = document.querySelectorAll('.collapsible');
var i;
for (i=0; i<buttons.length; i++) {
	buttons[i].addEventListener('click', toggleFeatured);
}