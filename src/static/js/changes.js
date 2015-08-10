
$(document).ready(function () {
    
    $.get( "/updating/retrieveUpdates", function( data ) {
        console.log(data);
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
});
