function clearFeatured() {
    $.post('/clear_featured').done(function() {
        location.reload(true)
        }).fail(function() {});
}

var clearButton = document.querySelector('#clear_featured');
clearButton.addEventListener('click', clearFeatured)