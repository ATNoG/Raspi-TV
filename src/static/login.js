$(document).ready(function(){
	$('#login').click(function(){
		var username = $('#userbox').val();
		var password = $('#userpass').val();
		$.post( "/idp/login", {user: username, pw: password}, function( data ) {
			data = JSON.parse(data);
            console.log(data);

			html = '<div class="alert alert-success" role="alert">'+data.response+'</div>';
            $("#message").html(html);
            $("#message").show("slow");
            setTimeout(function(){$(id).hide("slow")}, 2000);

            if (data.location!="/idp")
            	window.location.href = data.location;
        })
    })
})