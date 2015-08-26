$(document).ready(function(){
    get_info_twitter();
    $( "#tweets-table" ).sortable({
      revert: true
    });
    $( "ul, li" ).disableSelection();
});

function get_info_twitter() {
    $.get('/admin/get/tweets', function(data) {
        var html = "";
        for (var i = 0; i < data.length; i++) {
            html += "<li class='list-group-item'>" + data[i]['tweetid'] + " | <span class='author'>" + data[i]['author'] + "</span> | <span class='tweet'>" + data[i]['tweet'] + "</span>";
            if (data[i]['todisplay'] != 0) {
                $('#tweets-table').find('tbody').html(html);
            }
        }

    });
}