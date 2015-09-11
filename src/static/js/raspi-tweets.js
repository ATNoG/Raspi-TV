$(document).ready(function(){
    get_tweets();
});

function get_tweets() {
    $.get('/api/get_tweets', function(data){
        for (var i = 0; i < data.length; i++) {
            ('#tweets-table').append("<tr><strong>" + data[i]['author'] + "</strong>: " + data[i]['tweet'] + "</tr>");
        }
    });
}