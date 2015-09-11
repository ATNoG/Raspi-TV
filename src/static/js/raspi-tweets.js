$(document).ready(function(){
    var data_length = 0;
    var info = [];
    var counter = 0;


    function get_tweets() {
        $.getJSON('/api/get_tweets', function(data){
        data_length = data.length;
            for (var i = 0; i < data.length; i++) {
                info.push('<img src="img/img/twitter.png" width="2%"/>' + '<strong style=\'color:#003399;\'>' + ' ' + data[i]['author'] + '</strong>:' + '<span style=\'color:#003399;\'>' + data[i]['tweet'] + '</span>');
            }
            slider();
        });
    }

    function slider() {
            $('#tweets-table').html(info[counter]);

            setTimeout(function(){
                counter++;
                var $slideContainer = $('#tweets-table');
                var width = '-250%';

                if (counter == data_length) {
                    counter = 0;
                }
                $slideContainer.animate({'margin-left': width}, 5000, function(){
                        $slideContainer.css('margin-left', '0%');
                        slider();
                });


            }, 10000);

        }

    get_tweets();
});


