// Location Popover
$('#popover_location').popover({
    html: true,
    content: function () {
        return $('#pop_location-content').html();
    }
});
// Location Description Popover
$('#popover_location_description').popover({
    html: true,
    content: function () {
        return $('#pop_location_description-content').html();
    }
});
// Background Popover
$('#popover_background').popover({
    html: true,
    content: function () {
        return $('#pop_background-content').html();
    }
});


$(document).ready(function () {
    get_Updates();
});


var newLocation = "";
var newLocationDescription = "";
var newBackground = "";


function sendTo(id){
    
    if ($("#"+id).val().length <= 0 ){

        $('.error_box').removeClass('hide');
        $('.error_message').html("Enter Something");

    }else{

        $('.error_box').addClass('hide');

        newLocation = $('#new_location').val();
        newLocationDescription = $('#new_location_description').val();
        newBackground = $('#new_background').val();

        $.post('/admin/update/updateDB', {
            'location': newLocation,
            'locationDescription': newLocationDescription,
            'background': newBackground
        });
        
        location.reload();
    }


    get_Updates();
}


function get_Updates(){
    
    $.get('/api/get_HTMLChanges', function (data) {
        for (var i = 0; i < data.length; i++) {
            if (!data[i].type.localeCompare('text')) {
                $('#popover_' + data[i].id).html(data[i].content);
            } else if (data[i].type.localeCompare('image') == 0) {
                $("body").css('background-image', 'url(' + '/static/images' + data[i].content + ')');
            } else {
                //add , if needed
            }
        }
    });
}


