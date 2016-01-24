$(document).ready(function () {
    var error = getUrlVar('error');
    if (error) {
        $('.error_box').removeClass('hide');
        $('.error_message').html(error);
        window.location.hash = String(window.location.hash).replace('error=' + error + (window.location.hash.indexOf('error=' + error + '&') == -1 ? '' : '&'), '');
    }
    $.post('/admin/create/twitter', {'clear': 1});
});

$('#request-btn').click(function () {
    $.post('/admin/create/twitter', function (data) {
        window.open(data, '_blank');
    });
    $('.request').hide();
    $('.send').show();
});

$('#send-btn').click(function () {
    var pincode = $('#pincode').val();
    var note = $('#note').val();
    $.post('/admin/create/twitter', {'pincode': pincode, 'note': note}, function (data) {
        if (data == 'Successful') window.open('/admin/pages/accounts.html#twitter')
    });
});
