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
