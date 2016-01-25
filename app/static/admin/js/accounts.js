$(document).ready(function () {
    /* Dropbox */
    $.get('/admin/get/dropbox', function (data) {
        if (data == 'No account added.') {
            $('#dropbox-table').append(
                '<tr><th>No account added</th></tr>'
            );
        } else {
            $('#dropbox-table').append(
                '<tr><th>Authentication Token</th><td>' + data['AuthToken'] + '</td></tr>' +
                '<tr><th>Note</th><td>' + data['Note'] + '</td></tr>' +
                '<tr><th>Date</th><td>' + data['DateAdded'] + '</td></tr>'
            );
        }
    });

    /* Twitter */
    $.get('/admin/get/twitter', function (data) {
        if (data == 'No account added.') {
            $('#twitter-table').append(
                '<tr><th>No account added</th></tr>'
            );
        } else {
            $('#twitter-table').append(
                '<tr><th>Access Key</th><td>' + data['AccessKey'] + '</td></tr>' +
                '<tr><th>Access Secret</th><td>' + data['AccessSecret'] + '</td></tr>' +
                '<tr><th>Note</th><td>' + data['Note'] + '</td></tr>' +
                '<tr><th>Date</th><td>' + data['DateAdded'] + '</td></tr>'
            );
        }
    });
});
