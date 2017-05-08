# routing.py
from channels.staticfiles import StaticFilesConsumer
from messenger.consumers import ws_connect, ws_disconnect, ws_receive
from channels.routing import route



channel_routing = {
	#[
	# route("websocket.connect", ws_connect),
    # route("websocket.receive", ws_message),
    # route("websocket.disconnect", ws_disconnect),
	#]
	
	'http.request': StaticFilesConsumer(),
	'websocket.connect': ws_connect,
	'websocket.receive': ws_receive,
	'websocket.disconnect': ws_disconnect,
}

