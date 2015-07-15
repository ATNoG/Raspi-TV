$(document).ready(function(){
	var queue = [{'type': 'video', 'content': '<iframe width="853" height="480" src="https://www.youtube.com/embed/tUKmEi2azfQ?rel=0&amp;controls=0&amp;showinfo=0" frameborder="0" allowfullscreen></iframe>'},
				{'type': 'noticia', 'content': 'UA NOTICIA'}];
	var i = 0;

	var explode = function(){
		if(queue[i].type=="video"){
			$("#content").hide().html(queue[i].content).fadeIn('slow');
		}else{
			$("#content").hide().html(queue[i].content).fadeIn('slow');
		}
		console.log(i);
		i = (i+1)%queue.length;
		setTimeout(explode, 2000);
	};

	function get_news(){
        $.getJSON("/get_deti_news", function( data ) {
                console.log(data);
        });
    };

	explode();
	get_news();
});