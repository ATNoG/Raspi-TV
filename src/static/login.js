$(document).ready(function(){
	$('#login').click(function(){
		var username = $('#userbox').val();
		var password = $('#userpass').val();
		$.post( "/login", {user: username, pw: password}, function( data ) {
            data = JSON.parse(data);
            console.log(data);
		});
	});
});