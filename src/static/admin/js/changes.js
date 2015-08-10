//Location Popover
$('#popover_location').popover({
    html: true,
    content: function () {
        return $("#pop_location-content").html();
    }
});
//Location Descrition Popover
$('#popover_location_description').popover({
    html: true,
    content: function () {
        return $("#pop_location_description-content").html();
    }
//Background Popover
$('#popover_background').popover({
    html: true,
    content: function () {
        return $("#pop_background-content").html();
    }
});


$(document).ready(function () {
    
    $.get( "/retrieveUpdates", function( data ) {
            for(var i =0 ;i<data.length;i++){
                if(data[i].type.localeCompare('text') == 0){
                    $('#'+data[i].id).html(data[i].content);
                } else if (data[i].type.localeCompare('image')==0){
                    $("body").css('background-image', 'url(' +'/static/images'+ data[i].content + ')');
                } else {
                    //add , if needed
                }
            }
        });
    var newLocation= NaN;
    var newLocationDescription= NaN;
    var newBackground= NaN;

    $("#location_btn").click(function(){
        newLocation= $('#new_location').val();
    });
    $("#location_description_btn").click(function(){
        newLocationDescription= $('#new_location_description').val();
    });
    $("#background_btn").click(function(){
        newBackground= $('#new_background').val();
    });  

    $.post("/updateDB", {'location': newLocation, 'locationDescription': newLocationDescription},'background':newBackground);

});
