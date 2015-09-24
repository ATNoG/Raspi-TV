$(document).ready(function () {

});

$('#request-btn').click(function () {
    $.post('/admin/create/dropbox', function (data) {
        console.log(data);
        window.open(data,'_blank');
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
        console.log(data);
        if (data == 'Successful.') {
            window.location = '/admin/accounts.html#dropbox'
        } else {
            console.log(data)
        }
    });
});