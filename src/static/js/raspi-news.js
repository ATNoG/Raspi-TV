$(document).ready(function(){
	var queue = []
	var i = 0;

	function get_news(){
        $.getJSON("/api/get_deti_news").then(get_news_success);
    };

    function get_news_success(data){
    	console.log(data)
		for(var j=0; j<data.content.news.length; j++) {
			queue.push({'type' : 'noticia' , 'content' : data.content.news[j]});
		}
		for(var k=0; k<data.content.videos.length; k++) {
			queue.push({'type' : 'video' , 'content' : data.content.videos[k]});
		}

		explode();
    }

    var explode = function(){
    	var time_to_wait = 20000;

		if(queue[i].type=="video"){
			$("#content").hide().html('<video width="100%" controls autoplay> <source src="' + 'videos/' + queue[i].content.name + '.mp4' + '" type="video/ogg"> Your browser does not support HTML5 video. </video>').fadeIn('slow');
			var time = function(){
					setTimeout(function(){
						if(!$.isNumeric($("video")[0]["duration"])){
							time();
						}else{
							time_to_wait = $("video")[0]["duration"]*1000 + 1500;
							i = (i+1);
							if (i==queue.length) {
								i = 0;
							}
							setTimeout(explode, time_to_wait);
						}
					}, 100);
			};
			time();
		}else{
			$("#content").hide().html('<h2 style="color:#33B3D1">' + queue[i].content.title + '</h2>' + '<span style="color:#003399">' + queue[i].content.date + '</span>' + '<br>' + '<span style="color:#003399">' + queue[i].content.author + '</span>' + queue[i].content.summary).fadeIn('slow');
			i = (i+1);
			if (i==queue.length) {
				i = 0;
			}

			var peices_of_page = Math.ceil($(document).height()/$(window).height());
        	var count = 0;

        	var scroll = function(){
                setTimeout(function(){
                    $(document).scrollTop(count*$(window).height());

                    //console.log($(document).scrollTop());

                    count++;

                    if(count<peices_of_page){
                        scroll();
                    }
                }, 10000);
            };

        	scroll();
			setTimeout(explode, peices_of_page*time_to_wait);
		}

	};

	get_news();
});