$(function() {
	var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
	var chatsock = new ReconnectingWebSocket(ws_scheme + '://' + window.location.host + window.location.pathname);

	$('#chatform').on('submit', function(event) {
		//event.preventDefault();
		var message = {
			// handle: $('#handle').val(),
			message: $('#message').val(),
		}
		if (message.message != ''){
			chatsock.send(JSON.stringify(message));
			$('#message').val('');
		}

		
		return false;
	});

	chatsock.onmessage = function(message) {
		var data = JSON.parse(message.data);
		$('#chat').append('<tr>'
			/*+ '<td>' + data.timestamp + '</td>'*/
			+ '<td style="padding-bottom:15px;">' + data.handle + ':&nbsp' + '</td>'
			+ '<td style="padding-bottom:15px;">' + data.message + '</td>'
		+ '</tr>');
		var chat = $('#chatbody');
		chat.scrollTop(chat[0].scrollHeight);
	};
});