$('#logout').click(function () {
    $.post('/admin/logout');
    window.location.href = '/admin';
    return false;
});

$(document).ready(function () {
    admin_get('dropbox');
    admin_get('twitter');
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
