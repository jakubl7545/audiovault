function clear() {
    $.post('/clear').done(function() {
        location.reload(true)
        }).fail(function() {});
}

var clearButton = document.querySelector('#clear_featured');
clearButton.addEventListener('click', clear)