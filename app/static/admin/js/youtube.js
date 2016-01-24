$(document).ready(function () {
    var error = getUrlVar('error');
    if (error) {
        $('.error_box').removeClass('hide');
        $('.error_message').html(error);
        window.location.hash = String(window.location.hash).replace('error=' + error + (window.location.hash.indexOf('error=' + error + '&') == -1 ? '' : '&'), '');
    }

    var next = 1;

    function remove(btn) {
        var fieldID = "#field_input" + btn.id.replace("remove", "");
        var num = fieldID.split("#field_input");
        var link = $(fieldID).val();
        if (typeof link === 'undefined') {
            return;
        }
        $(fieldID).remove();
        $("#remove" + num[1]).remove();
        $.post("/youtube/delete_link", {link: link}, function (data) {
        });
    }

    $.getJSON("/api/get/list_of_links", function (data) {
        for (var i = 0; i < data.content.length; i++) {
            $("#field").after('<div class="input-group" id="field' + next + '"><input disabled id="field_input' + next + '" class="form-control" type="text">' + '<span class="input-group-btn"><button id="remove' + next + '" class="btn btn-danger remove-me" type="button">-</button></span></div>');
            $('#field_input' + next).val(data.content[i]);

            next = next + 1;
        }

        $(".remove-me").click(function () {
            remove(this);
        });
    });

    $(".add-more").click(function (e) {
        e.preventDefault();
        var link = $("#field_input").val();

        $.post("/youtube/save_link", {link: link}, function (data) {
            data = JSON.parse(data);

            if (data.status != 200) {
                alert('Your video couldn\'t be added! Verify if the URL is valid or if the video was already added.');
            } else {
                $('#field_input').val('');
                alert('Your video is in the queue to be downloaded, refresh to check if it\'s finished!');
            }
        });
    });
});

