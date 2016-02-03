////////////////////////////////////////////////////////
// Helper methods
////////////////////////////////////////////////////////

// Sets the current time
//
function updateTime() {
    var now = new Date();
    $('#date').text(now.toDateString());
    $('#time').text(now.toLocaleTimeString());
}
// Get tweets
//
function getTweets() {

    var tweets = [];
    var tweets_counter = 0;
    var data_length = 0;

    $.getJSON('/api/get/tweets', function (data) {
        data_length = data.length;

        for (var i = 0; i < data.length; i++)
            tweets.push('@<strong>' + data[i]['author'] + '</strong> ' + '<span>' + data[i]['tweet'] + '</span>');

        slider();
    });

    function slider() {
        var $tweet = $('#tweet');
        $tweet.html(tweets[tweets_counter++]);
        $tweet.fadeIn('slow');

        setTimeout(function () {
            $tweet.fadeOut('slow', function () {
                if (tweets_counter < data_length && tweets_counter < 30)
                    slider();
                else
                    getTweets();
            });
        }, 10000);
    }
}
// Get menus
//
function getCanteenMenus() {
    $.get('/api/get/canteen_menus', function (data) {
        for (var i = 0; i < data.length; i++) {
            var htmlCode = '<li class="dropdown"><a href="#" class="dropdown-toggle"><i class="fa fa-angle-double-right"></i><span class="hidden-xs">' + data[i]['info']['canteen'] + '</span></a></li><ul class="dropdown-menu">';
            for (var j = 0; j < data[i]['meal'].length; j++) {
                //if (typeof data[i]['meal'][j] == 'string')
                htmlCode += '<li><a class="ajax-link" href="#">' + data[i]['meal'][j] + '</a></li>';
            }
            htmlCode += '</ul></li>\n';
            $('#meals-container').append(htmlCode);
        }
    });
}
// Get settings
//
function getSettings() {
    $.get('/api/get/HTMLChanges', function (data) {
        for (var i = 0; i < data.length; i++) {
            if (data[i].type.localeCompare('text') == 0) {
                $('#' + data[i].id).html(data[i].content);
            } else if (data[i].type.localeCompare('image') == 0) {
                $('body').css('background-image', 'url(' + '/img' + data[i].content + ')');
            } else {
                //add , if needed
            }
        }
    });
}
// Set content size
//
function setContentSize() {
    var width_frame = $('#raspi-frame').width();
    var height_frame = 0.834 * $('#main').height();

    var $content_frame = $('#content_frame');
    $content_frame.width(width_frame);
    $content_frame.height(height_frame);

    // then load the iframe
    setTimeout(function () {
        $('#content_frame').attr('src', 'pages/news.html');
    }, 1000);
}

////////////////////////////////////////////////////////
// Main 'when ready' method
////////////////////////////////////////////////////////

$(document).ready(function () {

    setInterval(updateTime, 999);

    setContentSize();
    getCanteenMenus();
    getSettings();
    getTweets();
});
