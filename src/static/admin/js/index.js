$(document).ready(function () {
    get_user();
});

function get_user() {
    $.get('/user', function (data) {
        $('.username').html(data);
    });
}
