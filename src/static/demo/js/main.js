$(document).ready(function () {
    navigator.geolocation.getCurrentPosition(function (position) {
        var location = position.coords.latitude + ',' + position.coords.longitude;
        loadWeather(location);
        setInterval(loadWeather, 300000, location);
    });
});

function loadWeather(location, woeid) {
    $.simpleWeather({
        location: location,
        woeid: woeid,
        unit: 'c',
        success: function (weather) {
            html = '<h2><i class="weather icon-' + weather.code + '"></i> ' + weather.temp + '&deg;' + weather.units.temp + '</h2>';
            html += '<ul><li>' + weather.city + ', ' + weather.country + '</li>';
            html += '<li>' + weather.currently + '</li>';
            html += '<li>' + weather.wind.direction + ' ' + weather.wind.speed + ' ' + weather.units.speed + '</li></ul>';

            $('#weather').html(html);
        },
        error: function (error) {
            $('#weather').html('<p>' + error + '</p>');
        }
    });
}

$(document).ready(function () {
    $('.fc-button').hide();
});

$(document).ready(function () {
    setInterval(function () {
        var height = $('#sidebar').height() + $('.header').height() + 1;
        var max_height = $(document).height();
        console.log(max_height + ', ' + height);
        if(max_height - height)
            $('#sidebar-footer').css({ "margin-top": (max_height - height)});
    }, 5000);
});
