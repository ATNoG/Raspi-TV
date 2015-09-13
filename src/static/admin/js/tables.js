$(document).ready(function(){
    get_info_dropbox();
    get_info_twitter();

    $('#btn-update').click(function(){
       update_info();
    });
});

function get_info_twitter() {
    $.get('/admin/get/tweets', function(data) {
        var html = "";
        for (var i = 0; i < data.length; i++) {
            html += "<tr><td class='tweetid'>" + data[i]['tweetid'] + "</td><td class='author'>" + data[i]['author'] + "</td><td class='tweet'>" + data[i]['tweet'] + "</td>";
            if (data[i]['todisplay'] != 0) {
                html += "<td class='todisplay'><input type='checkbox' checked></td></tr>";
            } else {
                html += "<td class='todisplay'><input type='checkbox'></td></tr>";
            }
        }
        $('#tweets-table').find('tbody').html(html);
    });
}



function get_info_dropbox() {
    $.get('/admin/get/dropbox_files', function(data) {
        var html = "";
        for (var i = 0; i < data.length; i++) {
            html += "<tr><td class='filepath'>" + data[i]['filepath'] + "</td><td class='accountid'>" + data[i]['accountid'] + "</td>";
            if (data[i]['todisplay'] != 0) {
                html += "<td class='todisplay'><input type='checkbox' checked></td></tr>";
            } else {
                html += "<td class='todisplay'><input type='checkbox'></td></tr>";
            }
        }
        $('#dropbox_files-table').find('tbody').html(html);
    });
}


function update_info() {
    var dropbox = {
        files: get_dropbox_table()
    };
    var twitter = {
        tweetlist: get_tweets_table()
    };

    $.post('/admin/update/dropbox_files', dropbox, function(data) {
       if (data == 'Successful.') {
           // Success
       } else {
           // Error
       }
    });

    $.post('/admin/update/tweets', twitter, function(data) {
       if (data == 'Successful.') {
           // Success
       } else {
           // Error
       }
    });
}

function get_dropbox_table() {
    var $table_row = $('#dropbox_files-table').find('tbody').find('tr');
    var data_arr = [];

    $table_row.each(function() {
        var $elems = $(this).find('td');
        var filepath = $elems.find('.filepath').html();
        var accountid = $elems.find('.accountid').html();
        var todisplay;

        if ($elems.find('.todisplay').is(":checked")) {
            todisplay = 1;
        } else {
            todisplay = 0;
        }
        var elem_data = {
            filepath: filepath,
            accountid: accountid,
            todisplay: todisplay
        };

        data_arr.push(elem_data);
    });
    return data_arr;
}

function get_tweets_table() {
    var $table_row = $('#tweets-table').find('tbody').find('tr');
    var data_arr = [];

    $table_row.each(function() {
        var $elems = $(this).find('td');
        var tweetid = $elems.find('.tweetid').html();
        var author = $elems.find('.author').html();
        var tweet = $elems.find('.tweet').html();
        var todisplay;

        if ($elems.find('.todisplay').is(":checked")) {
            todisplay = 1;
        } else {
            todisplay = 0;
        }
        var elem_data = {
            tweetid: tweetid,
            author: author,
            tweet: tweet,
            todisplay: todisplay
        };

        data_arr.push(elem_data);
    });
    return data_arr;
}