$(document).ready(function(){
    var twitter_code = "<tr><td class='tweetid'>" + data[i]['tweetid'] + "</td><td class='author'>" + data[i]['author'] + "</td><td class='tweet'>" + data[i]['tweet'] + "</td>";
    var dropbox_code = "<tr><td class='filepath'>" + data[i]['filepath'] + "</td><td class='accountid'>" + data[i]['accountid'] + "</td>";

    get_info('tweets', twitter_code);
    get_info('dropbox_files', dropbox_code);

    $('#btn-update').click(function(){
       update_info();
    });
});

function get_info(query, input_code) {
    $.get('/admin/get/' + query, function(data) {
        var html = "";
        for (var i = 0; i < data.length; i++) {
            html += input_code;
            if (data[i]['todisplay'] != 0) {
                html += "<td class='todisplay'><input type='checkbox' checked></td></tr>";
            } else {
                html += "<td class='todisplay'><input type='checkbox'></td></tr>";
            }
        }
        $('#' + query + '-table').find('tbody').html(html);
    });
}


function update_info() {
    var dropbox = get_dropbox_table();
    var twitter = get_tweets_table();

    $.push('/admin/update/dropbox_files', dropbox, function(data) {
       if (data == 'Successful.') {
           // Success
       } else {
           // Error
       }
    });

    $.push('/admin/update/tweets', twitter, function(data) {
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

        if ($elems.find('.todisplay').attr('checked')) {
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

        if ($elems.find('.todisplay').attr('checked')) {
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