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
							console.log("espera");
						}else{
							time_to_wait = $("video")[0]["duration"]*1000 + 1500;
							console.log(i);
							i = (i+1);
							if (i==queue.length) {
								i = 0;
							}
							console.log(time_to_wait);
							setTimeout(explode, time_to_wait);
						}
					}, 100);
			};
			time();
		}else{
			$("#content").hide().html('<h2 style="color:#33B3D1">' + queue[i].content.title + '</h2>' + '<span style="color:#003399">' + queue[i].content.date + '</span>' + '<br>' + '<span style="color:#003399">' + queue[i].content.author + '</span>' + queue[i].content.summary).fadeIn('slow');
			console.log(i);
			i = (i+1);
			if (i==queue.length) {
				i = 0;
			}
			console.log(time_to_wait);
			setTimeout(explode, time_to_wait);
		}

	};

	get_news();
});