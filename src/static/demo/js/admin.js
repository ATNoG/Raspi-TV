$(document).ready(function () {
    get_user();
});

function get_user() {
    $.get('/admin/user', function (data) {
        console.log(data);
        data = JSON.parse(data);
        if(!data['user_id'])
            $('#user_info').html(
                '<li class="user-footer" style="text-align: center"> \
                    <div> \
                        <a href="/auth/login" class="btn btn-default btn-flat">Login</a> \
                    </div> \
                </li>'
            );
        else for(var key in data) $('.' + key).html(data[key]);
    });
}

function getUrlVar(name) {
    var url = window.location.hash == '' ? window.location.hash : window.location.hash.substring(1);
    var data = {};
    var fields = url.split('&');
    for(var i = 0; i < fields.length; i++){
        var entry = fields[i].split('=');
        data[entry[0]] = entry[1];
    }
    return data[name];
}
