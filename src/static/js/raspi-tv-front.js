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
			$("#content").hide().html('<h1 style="color:#003399">' + queue[i].content.title + '</h1>' + '<span style="color:#003399">' + queue[i].content.date + '</span>' + '<br>' + queue[i].content.author + queue[i].content.summary).fadeIn('slow');
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
    	}else if(data.content.weather.weather_code == 801){
    		$("#weather").html('<img src="img/img_met/sun_simple_cloudy.png" width="100%"/>');
    	}else if(data.content.weather.weather_code >= 802 && data.content.weather.weather_code <= 804 ){
    		$("#weather").html('<img src="img/img_met/cloud.png" width="100%"/>');
    	}else if((data.content.weather.weather_code >= 501 && data.content.weather.weather_code <= 531) || (data.content.weather.weather_code >= 300 && data.content.weather.weather_code >= 321)){
    		$("#weather").html('<img src="img/img_met/rain.png" width="100%"/>');
    	}else if(data.content.weather.weather_code == 500){
    		$("#weather").html('<img src="img/img_met/sun_simple_rain.png" width="100%"/>');
    	}else if(data.content.weather.weather_code >= 600 && data.content.weather.weather_code <= 622){
    		$("#weather").html('<img src="img/img_met/cloud_snow.png" width="100%"/>');
    	}else{
    		$("#weather").html('<img src="img/img_met/default.png" width="100%"/>');
    	}

		// icons from http://www.flaticon.com/search/haw-weather-fill

    	$("#hum").html('<img src="img/img_met/hum.png" width="15%"/>' + " " + '<big style="color:#003399" "font-size:3%">' +  data.content.weather.humidity + "%" + '</big>');
    	$("#temp").html('<img src="img/img_met/temp.png" width=15%"/>' + " " + '<big style="color:#003399" "font-size:3%">'+ data.content.weather.temperature.temp + " ºC" + '</big>');
    	$("#wind").html('<img src="img/img_met/wind.png" width="15%"/>'+ " " + '<big style="color:#003399" "font-size:3%">' + data.content.weather.wind.speed + " km/h" + '</big>');
    };

	get_news();
	get_weather();
});