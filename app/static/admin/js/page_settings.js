$(document).ready(function () {
    get_Updates();
});


$("#save_btn").click(function () {

    var newLocation = $('#location').val();
    var newLocationDescription = $('#location_description').val();
    var newWeather = $("#weatherR").val();
    var newFeedSource = $("#feed").val();

    if (newLocation.length <= 0 || newLocationDescription.length <= 0 || newWeather.length <= 0 || newFeedSource.length <= 0) {

        $('.error_box').removeClass('hide');
        $('.error_message').html("Specify All Fields Correctly");

    } else {

        $.post('/admin/update/updateDB', {
            'location': newLocation,
            'locationDescription': newLocationDescription,
            'weather': newWeather,
            'feed': newFeedSource
        });

        $(".success_box").removeClass('hide');

        get_Updates();
        location.reload();

    }
});


function get_Updates() {

    $.get('/api/get/HTMLChanges', function (data) {
        for (var i = 0; i < data.length; i++) {
            if (!data[i].type.localeCompare('text')) {
                $("#" + data[i].id).val(data[i].content);
            } else {
                //add , if needed
            }
        }
    });
}


