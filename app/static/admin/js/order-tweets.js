$(document).ready(function () {
    get_info_tweets();

    $('#btn-update').click(function () {
        $('.alert').hide();
        $('.loading-gif-container').show();
        update_info();
    });
});

function get_info_tweets() {
    $.get('/admin/get/tweets', function (data) {
        var $tweetTable = $("#tweets-table");
        for (var i = 0; i < data.length; i++) {
            var tweet = "<li class='list-group-item'><strong><span class='tweetid' style='display:none;'>" + data[i]['tweetid'] + "</span><span class='author'>" + data[i]['author'] + "</span></strong><br /><span class='tweet'>" + data[i]['tweet'] + "</span>";
            if (data[i]['todisplay']) {
                tweet += "<span class='to-display' style='float:right;'><input type='checkbox' checked></span></li>";
            } else {
                tweet += "<span class='to-display' style='float:right;'><input type='checkbox'></span></li>";
            }
            $tweetTable.append(tweet);
        }

        $tweetTable.sortable({
            revert: true
        });
        $("ul, li").disableSelection();
    });
}

function update_info() {
    var tweets = {
        tweetlist: JSON.stringify(get_tweets_table())
    };

    $.post('/admin/update/tweets', tweets, function (data) {
        $('.loading-gif-container').hide();
        if (data == 'Successful.') {
            $('#alert-success-created').show();
        } else {
            $('#alert-error-created').show();
        }
    });
}

function get_tweets_table() {
    var $table_row = $('#tweets-table').find('li');
    var data_arr = [];
    var i = 1;

    $table_row.each(function () {
        var tweetid = $(this).find('.tweetid').html();
        var author = $(this).find('.author').html();
        var tweet = $(this).find('.tweet').html();
        var todisplay = 0;
        var order = -1;

        if ($(this).find('.to-display').children().is(':checked')) {
            todisplay = 1;
            order = i;
            i++;
        } else console.log("Tweet skipped since it was not selected.");

        var elem_data = {
            'tweetid': tweetid,
            'author': author,
            'tweet': tweet,
            'todisplay': todisplay,
            'order': order
        };

        data_arr.push(elem_data);
    });
    return data_arr;
}