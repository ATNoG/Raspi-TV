$(document).ready(function(){
    get_info_dropbox('image', '#dropbox-images-table');
    get_info_dropbox('video', '#dropbox-videos-table');

    $('#btn-update').click(function(){
        $('.alert').hide();
        $('.loading-gif-container').show();
        update_info();
    });
});

function get_info_dropbox(type, table) {
    $.get('/admin/get/dropbox_files?file_type=' + type, function(data) {
        for (var i = 0; i < data.length; i++) {
            var code = "<li class='list-group-item'><span class='filepath'>" + data[i]['filepath'] + "</span>";
            if (data[i]['todisplay'] != 0) {
                code += "<span class='to-display' style='float:right;'><input type='checkbox' checked></span></li>";
            } else {
                code += "<span class='to-display' style='float:right;'><input type='checkbox'></span></li>";
            }
            $(table).append(code);
        }

        $(table).sortable({
            revert: true
        });
        $( "ul, li" ).disableSelection();
    });
}

function update_info() {
    var dropbox_files = {
        'images': JSON.stringify(get_dropbox_table('#dropbox-images-table')),
        'videos': JSON.stringify(get_dropbox_table('#dropbox-videos-table'))
    };


    $.post('/admin/update/dropbox_files', dropbox_files, function(data) {
        $('.loading-gif-container').hide();
        if (data == 'Successful.') {
            $('#alert-success-created').show();
        } else {
            $('#alert-error-created').show();
        }
    });
}

function get_dropbox_table(table) {
    var $table_row = $(table).find('li');
    var data_arr = [];
    var i = 1;

    $table_row.each(function() {
        var path = $(this).find('.filepath').html();
        var todisplay = 0;
        var order = -1;

        if ($(this).find('.to-display').children().is(':checked')) {
            todisplay = 1;
            order = i;
            i++;
        }

        var elem_data = {
            'filepath': path,
            'todisplay': todisplay,
            'order': order
        };

        data_arr.push(elem_data);
    });
    return data_arr;
}