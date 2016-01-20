var openButton = document.getElementById('opener');
var closerButton = document.getElementById('closer');
var send1 = document.getElementById('send1');
var ws;



openButton.onclick = function() {
	if ("WebSocket" in window) {
		var url = "ws://" + location.host + "/ws";
		ws = new WebSocket(url);
		ws.onopen = function() {
			//alert("Connection is open...");
		};
		ws.onmessage = function (evt) { 
			//var received_msg = evt.data;
			
		};
		ws.onclose = function() { 
		};
	} else {
		alert("WebSocket NOT supported by your Browser!");
	}
}

closerButton.onclick = function() {
	//alert("closing");
	ws.close()
}

send1.onclick = function() {
	ws.send("lolz");
}