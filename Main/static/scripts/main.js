
var openButton = document.getElementById('opener');
var closerButton = document.getElementById('closer');
var send1 = document.getElementById('send1');
var ws;
var frame = new Array(756); 


$(document).ready(function() {
	newWS();
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

function initCanvas() {
	var c = document.getElementById("myCanvas");
	var ctx = c.getContext("2d");
	ctx.fillStyle="lightgrey";
	ctx.fillRect(0,0,c.width,c.height);
	rectsize = parseInt(c.width/16);

	for (var i=0;i<16;i++){
		for (var j=0;j<16;j++){
			ctx.fillStyle = 'rgb(' + Math.floor(255-42.5*i) + ',' + Math.floor(255-42.5*j) + ',0)';
			ctx.fillRect((j*(rectsize))+1,(i*(rectsize))+1,rectsize-1,rectsize-1);
		}
	}
}

function refreshCanvas(frame) {
	var c = document.getElementById("myCanvas");
	var ctx = c.getContext("2d");
	ctx.clearRect(0, 0, c.width, c.height);
	ctx.fillStyle="black";
	ctx.fillRect(0,0,c.width,c.height);
	rectsize = parseInt(c.width/16);
	k=0;
	for (var i=0;i<16;i++){
		for (var j=0;j<16;j++){
			ctx.fillStyle = 'rgb(' + frame[k] + ',' + frame[k+1] + ',' + frame[k+2]+ ')';
			ctx.fillRect((j*(rectsize))+1,(i*(rectsize))+1,rectsize-1,rectsize-1);
			k+=3;
		}
	}
}

function update_config(config_string) {
	Metro.getPlugin("@color-selector").colorselector.options.returnValueType = "rgb";
	rgb_list =  JSON.parse(config_string)["highlight_color"]
	rgb_str = `rgb(${rgb_list[0]}, ${rgb_list[1]}, ${rgb_list[2]})`
	Metro.getPlugin("@color-selector").colorselector.val(rgb_str)
}

function newWS() {
	if ("WebSocket" in window) {
		var url = "ws://" + location.host + "/ws";
		ws = new WebSocket(url);
		ws.binaryType = "arraybuffer";
		ws.onopen = function() {
			//alert("Connection is open...");
			initCanvas();
			ws.send("ready_for_config")
		};
		ws.onmessage = function (evt) { 
			var received_msg = evt.data;
			if(evt.data instanceof ArrayBuffer){
				var frame = new Uint8Array(evt.data);
				refreshCanvas(frame);
			}
			else {
				console.log(evt.data)
				update_config(evt.data)
			}
		};
		ws.onclose = function() { 
		};
	} else {
		alert("WebSocket NOT supported by your Browser!");
	}
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
	ws.send("mediaflappy");
}
count.onclick = function(){
	ws.send("etcbincounter");
}
clock.onclick = function(){
	ws.send("etcclock");
}

function newMessage(form) {
    var message = form.formToDict();
    ws.send(JSON.stringify(message));
}


function on_color_picked() {
	color = color_selector.colorselector.rgb;
	ws.send(`highlight_color: ${color.r},${color.g},${color.b}`);
}

window.onload = function () {
	color_selector = Metro.getPlugin('@color-selector');
	Metro.getPlugin("@color-selector").colorselector.options.onSelectColor = on_color_picked
}