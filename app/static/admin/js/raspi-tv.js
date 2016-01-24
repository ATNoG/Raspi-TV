////////////////////////////////////////////////////////
// Helper methods
////////////////////////////////////////////////////////

// Updates user's info
//
function getUser() {
    $.get('/admin/user', function (data) {
        data = JSON.parse(data);
        for (var key in data)
            $('.' + key).html(data[key]);
    });
}

function getUrlVar(name) {
    var url = window.location.hash == '' ? window.location.hash : window.location.hash.substring(1);
    var data = {};
    var fields = url.split('&');
    for (var i = 0; i < fields.length; i++) {
        var entry = fields[i].split('=');
        data[entry[0]] = entry[1];
    }
    return data[name];
}

////////////////////////////////////////////////////////
// Main 'when ready' method
////////////////////////////////////////////////////////

$(document).ready(function () {
    getUser();
});
