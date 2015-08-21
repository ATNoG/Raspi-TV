$(document).ready(function(){
    var next = 1;
    $.getJSON("/api/list_of_ids", function( data ){
            console.log(data);
            for(var i=0; i<data.content.length; i++){
                 $("#field1").after('<div class="input-group" id="field' + next + '"><input id="field_input' + next + '" class="form-control" type="text">' + '<span class="input-group-btn"><button id="remove' + next + '" class="btn btn-danger remove-me" >-</button></span></div>');
                 $('#field_input' + next).val(data.content[i]);
                 next = next + 1;
            }
    });

    $(".add-more").click(function(e){
        e.preventDefault();
        var addto = "#field1";
        var addRemove = "#field_input" + next;
        var link = $("#field_input").val();
        var newIn = '<div class="input-group" id="field' + next + '"><input id="field_input' + next + '" class="form-control" placeholder="' + link  + '" type="text">';
        var newInput = $(newIn);

        var removeBtn = '<span class="input-group-btn"><button id="remove' + next + '" class="btn btn-danger remove-me" >-</button></span></div>';
        var removeButton = $(removeBtn);
        $(addto).after(newInput);
        $(addRemove).after(removeButton);
        $("#field" + next).attr('data-source',$(addto).attr('data-source'));
        next = next + 1;

            $('.remove-me').click(function(e){
                e.preventDefault();
                var fieldID = "#field" + this.id.replace("remove", "");
                $(fieldID).remove();
                console.log(fieldID);
            });

    });

    $("#b1").click(function(){

        var link = $("#field_input").val();
        $.post( "/youtube/saveId", {id: link}, function( data ) {
        });

        $('#field_input').val('');


    });

    $("#remove").click(function(){

        var link = $("#field_input").val();

        $.post( "/youtube/deleteId", link, function( data ) {
            console.log(data);
        });
    });

});
