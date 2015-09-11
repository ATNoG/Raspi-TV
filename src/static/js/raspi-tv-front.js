$(document).ready(function(){
	function get_weather(){
        $.getJSON("/api/get_weather").then(get_weather_success);
    };

    function get_weather_success(data){
		console.log(data);
    	var sunset_time = data.content.weather.sunset;
    	var sunrise_time = data.content.weather.sunrise;
		var time = Date();
		time = time.split(" ");
		time = time[4]

		if(time < sunset_time && time > sunrise_time){
			if(data.content.weather.status == 800){
				$("#weather").html('<img src="img/img_met/sun.png" width="50%"/>');
			}else if(data.content.weather.status == 801){
				$("#weather").html('<img src="img/img_met/sun_simple_cloudy.png" width="50%"/>');
			}else if(data.content.weather.status >= 802 && data.content.weather.status <= 804 ){
				$("#weather").html('<img src="img/img_met/cloud.png" width="50%"/>');
			}else if((data.content.weather.status >= 501 && data.content.weather.status <= 531) || (data.content.weather.status >= 300 && data.content.weather.status >= 321)){
				$("#weather").html('<img src="img/img_met/rain.png" width="50%"/>');
			}else if(data.content.weather.status == 500){
				$("#weather").html('<img src="img/img_met/sun_simple_rain.png" width="50%"/>');
			}else if(data.content.weather.status >= 600 && data.content.weather.status <= 622){
				$("#weather").html('<img src="img/img_met/cloud_snow.png" width="50%"/>');
			}else{
				$("#weather").html('<img src="img/img_met/default.png" width="50%"/>');
			}
    	}else{
    		if(data.content.weather.status == 800){
				$("#weather").html('<img src="img/img_met/moon.png" width="50%"/>');
			}else if(data.content.weather.status == 801){
				$("#weather").html('<img src="img/img_met/moon_cloudy.png" width="50%"/>');
			}else if(data.content.weather.status >= 802 && data.content.weather.status <= 804 ){
				$("#weather").html('<img src="img/img_met/cloud.png" width="50%"/>');
			}else if((data.content.weather.status >= 501 && data.content.weather.status <= 531) || (data.content.weather.status >= 300 && data.content.weather.status >= 321)){
				$("#weather").html('<img src="img/img_met/moon_rain.png" width="50%"/>');
			}else if(data.content.weather.status == 500){
				$("#weather").html('<img src="img/img_met/moon_rain.png" width="50%"/>');
			}else if(data.content.weather.status >= 600 && data.content.weather.status <= 622){
				$("#weather").html('<img src="img/img_met/cloud_snow.png" width="50%"/>');
			}else{
				$("#weather").html('<img src="img/img_met/default.png" width="50%"/>');
			}
    	}

		// icons from http://www.flaticon.com/search/haw-weather-fill

    	$("#hum").html('<img src="img/img_met/hum.png" width="15%"/>' + " " + '<big style="color:#33B3D1" "font-size:3%">' +  data.content.weather.humidity + "%" + '</big>');
    	$("#temp").html('<img src="img/img_met/temp.png" width=15%"/>' + " " + '<big style="color:#33B3D1" "font-size:3%">'+ data.content.weather.temperature + " ºC" + '</big>');
    	$("#wind").html('<img src="img/img_met/wind.png" width="15%"/>'+ " " + '<big style="color:#33B3D1" "font-size:3%">' + Math.round(data.content.weather.wind).toFixed(2) + " km/h" + '</big>');
    	$("#sunrise").html('<img src="img/img_met/sunrise.png" width="15%"/>'+ " " + '<big style="color:#33B3D1" "font-size:3%">' + data.content.weather.sunrise + "h" +'</big>');
    	$("#sunset").html('<img src="img/img_met/sunset.png" width="15%"/>'+ " " + '<big style="color:#33B3D1" "font-size:3%">' + data.content.weather.sunset + "h" + '</big>');

		setTimeout(function(){
			width_iframe = $("#content_div").width();
			$("#content_frame").width(width_iframe);
			//console.log("width");
			//console.log(width_iframe);

			height_frame = $("#right_bar").height();
			$("#content_frame").height(height_frame);
			//console.log("height");
			//console.log(height_frame);
		}, 100);

    };

	get_weather();

});