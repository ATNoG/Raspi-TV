$('#logout').click(function () {
    $.post('/admin/logout');
    window.location.href = '/admin';
    return false;
});

$(document).ready(function () {
    admin_get('dropbox');
    admin_get('twitter');

    // If there are any hash arguments on the URL, save the token
    if (window.location.hash.length != 0) {
        save_access_token();
    }
});

function admin_get(query) {
    $.get('/admin/get/' + query, function (data) {
        data = JSON.parse(data);
        var text = '';
        for (var i = 0; i < data.length; i++)
            text += '<tr><td>' + data[i]['account'] + '</td><td>' + data[i]['token'] + '</td><td>' + data[i]['date'] + '</td><td>' + data[i]['note'] + '</td></tr>';
        $('#' + query + '-table').append(text);
    });
}

function save_access_token() {
    var access_token = getURLHashInfo('access_token');
    var account_id = getURLHashInfo('uid');
    var data = {
        account: account_id,
        token: access_token,
        note: ""
    };
    $.post('/admin/create/dropbox', data, function(data) {
        if (data == 'Successful.') {
            // Show success message
        } else {
            // Show error message
        }
    });
}

function getURLHashInfo(field) {
    var url = window.location.hash.substring(1);
    var fields = url.split("&");
    for (var i = 0; i < fields.length; i++) {
        var parameters = fields[i].split("=");
        if (parameters[0] == field) {
            return parameters[1];
        }
    }
}