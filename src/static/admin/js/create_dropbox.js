$(document).ready(function () {
    // If there are any hash arguments on the URL, save the token
    if (window.location.hash.length != 0) {
        save_access_token();
    }
});

$('#request-btn').click(function () {
    $.post('/admin/create/dropbox', function (data) {
        console.log(data);
        window.location.href = data;
        //window.open(data,'_blank');
    });
});

function save_access_token() {
    var access_token = getURLHashInfo('access_token');
    var account_id = getURLHashInfo('uid');
    var params = {
        auth: 1,
        access_token: access_token,
        note: ""
    };
    $.post('/admin/create/dropbox', params, function (data) {
        console.log(data);
        if (data == 'Successful.') {
            window.location = 'http://localhost:8080/admin/accounts.html'
        } else {
            console.log(data)
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