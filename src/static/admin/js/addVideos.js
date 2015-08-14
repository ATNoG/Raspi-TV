$(document).ready(function(){
    var next = 1;
    $(".add-more").click(function(e){
        e.preventDefault();
        var addto = "#field1";
        next = next + 1;
        var addRemove = "#field_input" + (next);
        var newIn = '<div class="input-group" id="field' + next + '"><input id="field_input' + next + '" class="form-control" placeholder="Your YouTube URL" type="text">';
        var newInput = $(newIn);
        var removeBtn = '<span class="input-group-btn"><button id="remove' + next + '" class="btn btn-danger remove-me" >-</button></span></div>';
        var removeButton = $(removeBtn);
        $(addto).before(newInput);
        $(addRemove).after(removeButton);
        $("#field" + next).attr('data-source',$(addto).attr('data-source'));

            $('.remove-me').click(function(e){
                e.preventDefault();
                var fieldID = "#field" + this.id.replace("remove", "");
                $(fieldID).remove();
                console.log(fieldID);
            });

    });
    

    
});
