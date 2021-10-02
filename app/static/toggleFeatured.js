function toggleFeatured() {
	var content = this.nextElementSibling;
	if (content.style.display == "none") {
		this.setAttribute("aria-expanded", true);
		content.style.display = "block";
	} else {
		this.setAttribute("aria-expanded", false);
		content.style.display = "none";
	}
}
var buttons = document.querySelectorAll('.collapsible');
var i;
for (i=0; i<buttons.length; i++) {
	buttons[i].addEventListener('click', toggleFeatured);
}