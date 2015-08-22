$(document).ready(function () {
    get_Updates();
});


$("#save_btn").click(function(){

   var newLocation = $('#location').val();
   var newLocationDescription = $('#location_description').val();
   var newBackground = $('#background').val();
   var newWeather = $("#weather").val();

    if (newLocation.length<=0 || newLocationDescription.length<=0 || newBackground.length<=0 || newWeather.length<=0){

        $('.error_box').removeClass('hide');
        $('.error_message').html("Specify All Fields Correctly");

    }else{

        $.post('/admin/update/updateDB', {
            'location': newLocation,
            'locationDescription': newLocationDescription,
            'background': newBackground,
            'weather': newWeather
        });
        
        $(".success_box").removeClass('hide');

        get_Updates();
        location.reload();
        
    }
});


function get_Updates(){
    
    $.get('/api/get_HTMLChanges', function (data) {
        for (var i = 0; i < data.length; i++) {
            if (!data[i].type.localeCompare('text')) {
                $("#"+data[i].id).val(data[i].content);
            } else if (data[i].type.localeCompare('image') == 0) {
                //$("body").css('background-image', 'url(' + '/static/images' + data[i].content + ')');
            } else {
                //add , if needed
            }
        }
    });
}


