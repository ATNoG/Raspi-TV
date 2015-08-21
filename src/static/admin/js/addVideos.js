$(document).ready(function(){
    var next = 1;

    $.getJSON("/api/list_of_ids", function( data ){
            console.log(data);
            for(var i=0; i<data.content.length; i++){
                 $("#field").after('<div class="input-group" id="field' + next + '"><input id="field_input' + next + '" class="form-control" type="text">' + '<span class="input-group-btn"><button id="remove' + next + '" class="btn btn-danger remove-me" type="button">-</button></span></div>');
                 $('#field_input' + next).val(data.content[i]);
                 next = next + 1;
            }

        $(".remove-me").click(function(){
                    var fieldID = "#field_input" + this.id.replace("remove", "");
                    var num = fieldID.split("#field_input");
                    console.log(fieldID);
                    var tmp = $(fieldID).val();
                    console.log(tmp);
                    $(fieldID).remove();
                    $("#remove" + num[1]).remove();
                    //$.post( "/youtube/deleteId", link, function( data ) {
                    //});
        });

    });

    $(".add-more").click(function(e){
        e.preventDefault();
        var addto = "#field";
        var addRemove = "#field_input" + next;
        var link = $("#field_input").val();
        var newIn = '<div class="input-group" id="field' + next + '"><input id="field_input' + next + '" class="form-control" type="text">';
        var newInput = $(newIn);

        var removeBtn = '<span class="input-group-btn"><button id="remove' + next + '" class="btn btn-danger remove-me" >-</button></span></div>';
        var removeButton = $(removeBtn);
        $(addto).after(newInput);
        $('#field_input' + next).val(link);
        $(addRemove).after(removeButton);
        $("#field" + next).attr('data-source',$(addto).attr('data-source'));
        next = next + 1;

        $.post( "/youtube/saveId", {id: link}, function( data ) {
        });

        $('#field_input').val('');

    });



    //$("#remove" + 1).click(function(){
    //    console.log("passou");
    //    var link = $("#field_input").val();

//        $.post( "/youtube/deleteId", link, function( data ) {
  //          console.log(data);
    //    });
    //});

});
