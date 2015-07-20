function showPassword() {
    
    var key_attr = $('#userpass').attr('type');
    
    if(key_attr != 'text') {
        
        $('.checkbox').addClass('show');
        $('#userpass').attr('type', 'text');
        
    } else {
        
        $('.checkbox').removeClass('show');
        $('#userpass').attr('type', 'password');
        
    }
    
}

$(document).ready(function(){
	$('#btn-login').click(function(){
		var username = $('#userbox').val();
		var password = $('#userpass').val();
		$.post( "/idp/login", {user: username, pw: password}, function( data ) {
			data = JSON.parse(data);
            console.log(data);

			html = '<div class="alert alert-success" role="alert">'+data.response+'</div>';
            $("#message").html(html);
            $("#message").show("slow");
            setTimeout(function(){$(id).hide("slow")}, 500);

            if (data.location!="/idp")
            	window.location.href = data.location;
        })
    })
})