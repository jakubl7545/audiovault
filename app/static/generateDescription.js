function generate() {
    var title = document.getElementById('name');
    var description = document.getElementById('description');
    $.post('/generate_description', {'title': title.value
    }).done(function(response) {
        description.value += `${response['description']}`
    }).fail(function() {});
}

var generateButton = document.querySelector('#generate_description');
generateButton.addEventListener('click', generate);