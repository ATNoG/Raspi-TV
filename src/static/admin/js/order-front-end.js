$(document).ready(function(){
    get_info_services();


    $('#btn-update').click(function(){
       update_info();
    });
});

function get_info_services() {
    $.get('/admin/get/services', function(data) {
        for (var i = 0; i < data.length; i++) {
            var code = "<li class='list-group-item'><span class='service-name'>" + data[i]['name'] + "</span>";
            if (data[i]['todisplay'] != 0) {
                code += "<span class='to-display' style='float:right;'><input type='checkbox' checked></span></li>";
            } else {
                code += "<span class='to-display' style='float:right;'><input type='checkbox'></span></li>";
            }
            $('#services-table').append(code);
        }

        $("#services-table").sortable({
          revert: true
        });
        $( "ul, li" ).disableSelection();
    });
}

function update_info() {
    var services = {
        servicelist: JSON.stringify(get_services_table())
    };

    console.log(services);
    $.post('/admin/update/services', services, function(data) {
       console.log(data);
       if (data == 'Successful.') {
           // Success
       } else {
           // Error
       }
    });
}

function get_services_table() {
    var $table_row = $('#services-table').find('li');
    var data_arr = [];
    var i = 1;

    $table_row.each(function() {
        var name = $(this).find('.service-name').html();
        var todisplay = 0;
        var order = -1;

        if ($(this).find('.to-display').children().is(':checked')) {
            todisplay = 1;
            order = i;
            i++;
        }

        var elem_data = {
            'name': name,
            'todisplay': todisplay,
            'order': order
        };

        data_arr.push(elem_data);
    });
    return data_arr;
}