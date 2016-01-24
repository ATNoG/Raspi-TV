// Password Popover
$('#popover_password').popover({
    html: true,
    content: function () {
        return $("#pop_password-content").html();
    }
});
// First Name Popover
$('#popover_first').popover({
    html: true,
    content: function () {
        return $("#pop_first-content").html();
    }
});
// Last Name Popover
$('#popover_last').popover({
    html: true,
    content: function () {
        return $("#pop_last-content").html();
    }
});
// Email Popover
$('#popover_email').popover({
    html: true,
    content: function () {
        return $("#pop_email-content").html();
    }
});
// Check Passwords
function check_passwords() {
    var password = $("#new_password").val();
    var confirmPassword = $("#new_password_repeat").val();

    if (!password.length)
        $("#password_btn").addClass("disabled").html('Password field is empty');
    else if (password != confirmPassword)
        $("#password_btn").addClass("disabled").html('Passwords don\'t match');
    else
        $("#password_btn").removeClass("disabled").html('Change password');
}

$(document).ready(function () {
    var error = getUrlVar('error');
    if (error) {
        $('.error_box').removeClass('hide');
        $('.error_message').html(decodeURI(error));
        window.location.hash = String(window.location.hash).replace('error=' + error + (window.location.hash.indexOf('error=' + error + '&') == -1 ? '' : '&'), '');
    }
});
