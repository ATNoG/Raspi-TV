$('#request-btn').click(function () {
    $.post('/admin/create/dropbox', function (data) {
        window.open(data, '_blank');
    });
    $('.request').hide();
    $('.send').show();
});

$('#send-btn').click(function () {
    var params = {
        auth: 1,
        pincode: $('#pincode').val(),
        note: $('#note').val()
    };
    $.post('/admin/create/dropbox', params, function (data) {
        if (data == 'Successful.') window.location = '/admin/pages/accounts.html#dropbox'
    });
});
