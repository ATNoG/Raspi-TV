$(document).ready(function(){
    get_info_twitter();
    get_info_dropbox();
    $( "#tweets-table" ).sortable({
      revert: true
    });
    $( "ul, li" ).disableSelection();

    $('#btn-update').click(function(){
       update_info();
    });
});

function get_info_twitter() {
    $.get('/admin/get/tweets', function(data) {
        var html = "";
        for (var i = 0; i < data.length; i++) {
            html += "<li class='list-group-item'><span class='tweetid'>" + data[i]['tweetid'] + "</span> | <span class='author'>" + data[i]['author'] + "</span> | <span class='tweet'>" + data[i]['tweet'] + "</span></li>";
            if (data[i]['todisplay'] != 0) {
                $('#tweets-table').append(html);
            }
        }
    });
}

function get_info_dropbox() {
    $.get('/admin/get/dropbox_files', function(data) {
        var html = "";
        for (var i = 0; i < data.length; i++) {
            html += "<li class='list-group-item'><span class='filepath'>" + data[i]['filepath'] + "</span> | <span class='accountid'>" + data[i]['accountid'] + "</span></li>";
            if (data[i]['todisplay'] != 0) {
                $('#dropbox-table').append(html);
            }
        }
    });
}

function update_info() {
    var dropbox = {
        files: get_dropbox_table()
    };
    var twitter = {
        tweetlist: get_tweets_table()
    };

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

function get_tweets_table() {
    var $table_row = $('#tweets-table').find('li');
    var data_arr = [];
    var i = 0;

    $table_row.each(function() {
        var tweetid = $table_row.find('.tweetid').html();
        var author = $table_row.find('.author').html();
        var tweet = $table_row.find('.tweet').html();
        var todisplay = 1;

        var elem_data = {
            tweetid: tweetid,
            author: author,
            tweet: tweet,
            todisplay: todisplay,
            order: i
        };

        data_arr.push(elem_data);
        i++;
    });
    return data_arr;
}

function get_dropbox_table() {
    var $table_row = $('#dropbox-table').find('li');
    var data_arr = [];
    var i = 0;

    $table_row.each(function() {
        var filepath = $table_row.find('.filepath').html();
        var accountid = $table_row.find('.accountid').html();
        var todisplay = 1;

        var elem_data = {
            filepath: filepath,
            accountid: accountid,
            todisplay: todisplay,
            order: i
        };

        data_arr.push(elem_data);
        i++;
    });
    return data_arr;
}