$(document).ready(function(){
	var queue = [];
	var i = 0;

    function get_all_info() {
        $.getJSON('/api/get_all_info').then(get_ordered);
	}

    function get_ordered(data) {
        console.log(data);
        for (var j = 0; j < data.length; j++) {
            console.log(data[j]['name']);
            switch(data[j]['name']) {
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
        console.log(queue);
        explode();
    }

    function queue_process_news(data) {
        for (var j = 0; j < data.content.news.length; j++) {
            queue.push({'type': 'noticia', 'content': data.content.news[j]});
        }
    }

    function queue_process_videos(data) {
        for(var j=0; j < data.content.length; j++) {
            queue.push({'type' : 'video' , 'content' : data.content[j]});
        }
    }

    function queue_process_images(data) {
        for(var j=0; j < data.content.length; j++) {
            queue.push({'type' : 'image' , 'content' : data.content[j]});
        }
    }

    var explode = function(){
    	var time_to_wait = 20000;

		if (queue[i].type=="video") {
            $("#content").hide().html('<video width="100%" controls autoplay> <source src="' + queue[i].content.filepath + '" type="video/ogg"> Your browser does not support HTML5 video. </video>').fadeIn('slow');
            var time = function () {
                setTimeout(function () {
                    if (!$.isNumeric($("video")[0]["duration"])) {
                        time();
                    } else {
                        time_to_wait = $("video")[0]["duration"] * 1000 + 1500;
                        i = (i + 1);
                        if (i == queue.length) {
                            i = 0;
                        }
                        setTimeout(explode, time_to_wait);
                    }
                }, 100);
            };
            time();

        } else if (queue[i].type == 'image') {
            $("#content").hide().html("<img src='" + queue[i].content.filepath + "'/>").fadeIn('slow');
            setTimeout(function(){
                i++;
                setTimeout(explode, 1000);
            }, 5000);
        } else {
			$("#content").hide().html('<h2 style="color:#33B3D1">' + queue[i].content.title + '</h2>' + '<span style="color:#003399">' + queue[i].content.date + '</span>' + '<br>' + '<span style="color:#003399">' + queue[i].content.author + '</span>' + queue[i].content.summary).fadeIn('slow');
			i = (i+1);
			if (i==queue.length) {
				i = 0;
			}

			var pieces_of_page = Math.ceil($(document).height()/$(window).height());
        	var count = 0;

        	var scroll = function(){
                setTimeout(function(){
                    $(document).scrollTop(count*$(window).height());

                    //console.log($(document).scrollTop());

                    count++;

                    if(count<pieces_of_page){
                        scroll();
                    }
                }, 10000);
            };

        	scroll();
			setTimeout(explode, pieces_of_page*time_to_wait);
		}

	};

	get_all_info();
});