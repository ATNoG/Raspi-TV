////////////////////////////////////////////////////////
// Global variables
////////////////////////////////////////////////////////

var i;
var queue;

////////////////////////////////////////////////////////
// Helper methods
////////////////////////////////////////////////////////

function get_all_info() {
    i = 0;
    queue = [];
    $.get('/api/get/all_info').then(get_ordered);
}

function get_ordered(data) {
    for (var j = 0; j < data.length; j++) {
        switch (data[j]['name']) {
            case 'News':
                queue_process_news(data[j]);
                break;

            case 'Youtube':
                queue_process_videos(data[j]);
                break;

            case 'Dropbox Videos':
                queue_process_videos(data[j]);
                break;

            case 'Dropbox Photos':
                queue_process_images(data[j]);
                break;
        }
    }

    explode();
}

function queue_process_news(data) {
    for (var j = 0; j < data.content.length; j++) {
        queue.push({'type': 'noticia', 'content': data.content[j]});
    }
}

function queue_process_videos(data) {
    for (var j = 0; j < data.content.length; j++) {
        queue.push({'type': 'video', 'content': data.content[j]});
    }
}

function queue_process_images(data) {
    for (var j = 0; j < data.content.length; j++) {
        queue.push({'type': 'image', 'content': data.content[j]});
    }
}

function explode() {
    if (i == queue.length)
        location.reload(true);

    if (queue[i].type == 'video') {
        $('#content').hide().html('<video width="100%" controls autoplay><source src="' + queue[i].content.filepath + '" type="video/ogg">Your browser does not support HTML5 video.</video>').fadeIn('slow');

        function time() {
            var $video = $('video')[0];

            if (!$.isNumeric($video['duration']))
                setTimeout(time, 500);
            else {
                i++;
                setTimeout(explode, $video['duration'] * 1000 + 1500);
            }
        }

        time();
    } else if (queue[i].type == 'image') {
        $('#content').hide().html('<img src="../data/dropbox_files' + queue[i].content.filepath + '"/>').fadeIn('slow');

        i++;
        setTimeout(explode, 5000);
    } else {
        $('#content').hide().html('<h2 style="color:#00904B">' + queue[i].content.title + '</h2>' + '<span style="color:#003399">' + queue[i].content.date + '</span>' + '<br>' + '<span style="color:#003399">' + queue[i].content.author + '</span>' + queue[i].content.summary).fadeIn('slow');

        var pieces_of_page = Math.ceil($(document).height() / $(window).height());
        var count = 0;

        var scroll = function () {
            setTimeout(function () {
                $(document).scrollTop(count * $(window).height());

                count++;
                if (count < pieces_of_page)
                    scroll();
            }, 10000);
        };

        scroll();
        i++;
        setTimeout(explode, pieces_of_page * 20000);
    }
}

////////////////////////////////////////////////////////
// Main 'when ready' method
////////////////////////////////////////////////////////

$(document).ready(function () {
    get_all_info();
});