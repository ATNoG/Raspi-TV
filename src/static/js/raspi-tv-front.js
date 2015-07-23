$(document).ready(function(){
	var queue = []
	var i = 0;

	function get_news(){
        $.getJSON("/api/get_deti_news").then(get_news_success);
    };

    function get_news_success(data){
		for(var j=0; j<data.content.news.length; j++) {
			queue.push({'type' : 'noticia' , 'content' : data.content.news[j]});
		}

		explode();
    }

    var explode = function(){
		if(queue[i].type=="video"){
			$("#content").hide().html(queue[i]).fadeIn('slow');
		}else{
			$("#content").hide().html(queue[i].content.title + queue[i].content.date + queue[i].content.author + queue[i].content.summary).fadeIn('slow');
			}
		console.log(i);
		i = (i+1);
		if (i==queue.length) {
			i = 0;
		}
		setTimeout(explode, 20000);
	};

	function get_weather(){
        $.getJSON("/api/get_weather").then(get_weather_success);
    };

    function get_weather_success(data){
    	console.log(data);
    	if(data.content.weather.weather_code == 800){
			$("#weather").html('<img src="img/img_met/sun.png" width="100%"/>');
    	}
    };

	get_news();
	get_weather();
});