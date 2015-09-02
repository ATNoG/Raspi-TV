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

	function get_weather(){
        $.getJSON("/api/get_weather").then(get_weather_success);
    };

    function get_weather_success(data){

    	var sunset_time = data.content.weather.sunset;
    	var sunrise_time = data.content.weather.sunrise;
		var time = Date();
		time = time.split(" ");
		time = time[4]

		if(time < sunset_time && time > sunrise_time){
			if(data.content.weather.status == 800){
				$("#weather").html('<img src="img/img_met/sun.png" width="100%"/>');
			}else if(data.content.weather.status == 801){
				$("#weather").html('<img src="img/img_met/sun_simple_cloudy.png" width="100%"/>');
			}else if(data.content.weather.status >= 802 && data.content.weather.status <= 804 ){
				$("#weather").html('<img src="img/img_met/cloud.png" width="100%"/>');
			}else if((data.content.weather.status >= 501 && data.content.weather.status <= 531) || (data.content.weather.status >= 300 && data.content.weather.status >= 321)){
				$("#weather").html('<img src="img/img_met/rain.png" width="100%"/>');
			}else if(data.content.weather.status == 500){
				$("#weather").html('<img src="img/img_met/sun_simple_rain.png" width="100%"/>');
			}else if(data.content.weather.status >= 600 && data.content.weather.status <= 622){
				$("#weather").html('<img src="img/img_met/cloud_snow.png" width="100%"/>');
			}else{
				$("#weather").html('<img src="img/img_met/default.png" width="100%"/>');
			}
    	}else{
    		if(data.content.weather.status == 800){
				$("#weather").html('<img src="img/img_met/moon.png" width="100%"/>');
			}else if(data.content.weather.status == 801){
				$("#weather").html('<img src="img/img_met/moon_cloudy.png" width="100%"/>');
			}else if(data.content.weather.status >= 802 && data.content.weather.status <= 804 ){
				$("#weather").html('<img src="img/img_met/cloud.png" width="100%"/>');
			}else if((data.content.weather.status >= 501 && data.content.weather.status <= 531) || (data.content.weather.status >= 300 && data.content.weather.status >= 321)){
				$("#weather").html('<img src="img/img_met/moon_rain.png" width="100%"/>');
			}else if(data.content.weather.status == 500){
				$("#weather").html('<img src="img/img_met/moon_rain.png" width="100%"/>');
			}else if(data.content.weather.status >= 600 && data.content.weather.status <= 622){
				$("#weather").html('<img src="img/img_met/cloud_snow.png" width="100%"/>');
			}else{
				$("#weather").html('<img src="img/img_met/default.png" width="100%"/>');
			}
    	}

		// icons from http://www.flaticon.com/search/haw-weather-fill

    	$("#hum").html('<img src="img/img_met/hum.png" width="15%"/>' + " " + '<big style="color:#33B3D1" "font-size:3%">' +  data.content.weather.humidity + "%" + '</big>');
    	$("#temp").html('<img src="img/img_met/temp.png" width=15%"/>' + " " + '<big style="color:#33B3D1" "font-size:3%">'+ data.content.weather.temperature + " ºC" + '</big>');
    	$("#wind").html('<img src="img/img_met/wind.png" width="15%"/>'+ " " + '<big style="color:#33B3D1" "font-size:3%">' + data.content.weather.wind + " km/h" + '</big>');
    	$("#sunrise").html('<img src="img/img_met/sunrise.png" width="15%"/>'+ " " + '<big style="color:#33B3D1" "font-size:3%">' + data.content.weather.sunrise + "h" +'</big>');
    	$("#sunset").html('<img src="img/img_met/sunset.png" width="15%"/>'+ " " + '<big style="color:#33B3D1" "font-size:3%">' + data.content.weather.sunset + "h" + '</big>');


    };

	get_news();
	get_weather();
});