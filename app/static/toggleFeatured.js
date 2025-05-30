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

for (let button of document.querySelectorAll('.collapsible')) {
	button.addEventListener('click', toggleFeatured);
}