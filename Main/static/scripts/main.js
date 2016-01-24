var openButton = document.getElementById('opener');
var closerButton = document.getElementById('closer');
var send1 = document.getElementById('send1');
var ws;

alert(location.host)

$(document).ready(function() {
	$(document).keydown(function(e) {
		switch(e.which) {
			case 37: // left
				ws.send("dirl");
				break;

			case 38: // up
				ws.send("diru");
				break;

			case 39: // right
				ws.send("dirr");
				break;

			case 40: // down
				ws.send("dird");
				break;

			default: return; // exit this handler for other keys
		}
		e.preventDefault(); // prevent the default action (scroll / move caret)
	});
});

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
	ws.send("gamesnake");
}
send2.onclick = function() {
	ws.send("medianyancat");
}
send3.onclick = function() {
	ws.send("mediatetris");
}
send4.onclick = function() {
	ws.send("mediaflappe");
}


function newMessage(form) {
    var message = form.formToDict();
    ws.send(JSON.stringify(message));
}
