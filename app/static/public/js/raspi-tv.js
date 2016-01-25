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

////////////////////////////////////////////////////////
// Main 'when ready' method
////////////////////////////////////////////////////////

$(document).ready(function () {

    setInterval(updateTime, 999);

    function setContentSize(data) {
        setTimeout(function () {
            var width_frame = $("#raspi-frame").width();
            var height_frame = $("#main-row").height();

            var $content_frame = $("#content_frame");
            $content_frame.width(width_frame);
            $content_frame.height(height_frame);
        }, 5000);

        // then call the changes
        setTimeout(function () {
            changes();
        }, 500);
    }


    // Changes
    //
    function changes() {
        $.get("/api/get/HTMLChanges", function (data) {
            for (var i = 0; i < data.length; i++) {
                if (data[i].type.localeCompare('text') == 0) {
                    $('#' + data[i].id).html(data[i].content);
                } else if (data[i].type.localeCompare('image') == 0) {
                    $("body").css('background-image', 'url(' + '/img' + data[i].content + ')');
                } else {
                    //add , if needed
                }
            }

            // then call get tweets
            setTimeout(function () {
                get_tweets();
            }, 500);
        });
    }

    var data_length = 0;
    var info = [];

    function get_tweets() {
        $.getJSON('/api/get/tweets', function (data) {
            data_length = data.length;

            for (var i = 0; i < data.length; i++) {
                info.push('<strong style="color:#003399;">' + data[i]['author'] + '</strong>:' + '<span style="color:#003399;">' + data[i]['tweet'] + '</span>');
            }
            slider();

            // then load the iframe
            setTimeout(function () {
                $("#content_frame").attr("src", "pages/news.html");
            }, 500);
        });
    }

    var counter = 0;

    function slider() {
        var $tweet = $("#tweet");
        $tweet.html(info[counter++]);
        $tweet.fadeIn();

        if (counter == data_length)
            counter = 0;

        setTimeout(function () {
            $tweet.fadeOut();
            slider();
        }, 10000);


    }

    setContentSize();
});