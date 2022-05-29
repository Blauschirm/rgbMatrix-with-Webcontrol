
var openButton = document.getElementById('opener');
var closerButton = document.getElementById('closer');
var send1 = document.getElementById('send1');
var ws;
var frame = new Array(756);
var old_config = {};
var config = {};
var change_in_progress = false;

$(document).ready(function () {
	newWS();
	$(document).keydown(function (e) {
		switch (e.which) {
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
	ctx.fillStyle = "lightgrey";
	ctx.fillRect(0, 0, c.width, c.height);
	rectsize = parseInt(c.width / 16);

	for (var i = 0; i < 16; i++) {
		for (var j = 0; j < 16; j++) {
			ctx.fillStyle = 'rgb(' + Math.floor(255 - 42.5 * i) + ',' + Math.floor(255 - 42.5 * j) + ',0)';
			ctx.fillRect((j * (rectsize)) + 1, (i * (rectsize)) + 1, rectsize - 1, rectsize - 1);
		}
	}
}

function refreshCanvas(frame) {
	var c = document.getElementById("myCanvas");
	var ctx = c.getContext("2d");
	ctx.clearRect(0, 0, c.width, c.height);
	ctx.fillStyle = "black";
	ctx.fillRect(0, 0, c.width, c.height);
	rectsize = parseInt(c.width / 16);
	k = 0;
	for (var i = 0; i < 16; i++) {
		for (var j = 0; j < 16; j++) {
			ctx.fillStyle = 'rgb(' + frame[k] + ',' + frame[k + 1] + ',' + frame[k + 2] + ')';
			ctx.fillRect((j * (rectsize)) + 1, (i * (rectsize)) + 1, rectsize - 1, rectsize - 1);
			k += 3;
		}
	}
}

function update_config(config_string) {
	config_change = JSON.parse(config_string)

	for (checkbox of $(".config_checkbox")) {
		var cb_name = checkbox.children[0].id
		if (cb_name in config_change && typeof config_change[cb_name] == "boolean") {
			checkbox.children[0].checked = config_change[cb_name]
		}
	}
	if ("config_colors_highlight" in config_change){
		change_in_progress = true
		Metro.getPlugin("@color-selector").colorselector.options.returnValueType = "rgb";
		rgb_list = config_change["config_colors_highlight"]
		rgb_str = `rgb(${rgb_list[0]}, ${rgb_list[1]}, ${rgb_list[2]})`
		Metro.getPlugin("@color-selector").colorselector.val(rgb_str)
		setTimeout(() => {
			change_in_progress = false
		}, 500);
	}
	config = {...config, ...config_change}

}

function newWS() {
	if ("WebSocket" in window) {
		var url = "ws://" + location.host + "/ws";
		ws = new WebSocket(url);
		ws.binaryType = "arraybuffer";
		ws.onopen = function () {
			//alert("Connection is open...");
			initCanvas();
			ws.send("ready_for_config")
		};
		ws.onmessage = function (evt) {
			var received_msg = evt.data;
			if (evt.data instanceof ArrayBuffer) {
				var frame = new Uint8Array(evt.data);
				refreshCanvas(frame);
			}
			else {
				console.log(evt.data)
				update_config(evt.data)
			}
		};
		ws.onclose = function () {
		};
	} else {
		alert("WebSocket NOT supported by your Browser!");
	}
}


send1.onclick = function () {
	ws.send("gamesnake");
}
send2.onclick = function () {
	ws.send("medianyancat");
}
send3.onclick = function () {
	ws.send("mediatetris");
}
send4.onclick = function () {
	ws.send("mediaflappy");
}
count.onclick = function () {
	ws.send("etcbincounter");
}
clock.onclick = function () {
	ws.send("etcclock");
}

function newMessage(form) {
	var message = form.formToDict();
	ws.send(JSON.stringify(message));
}

function on_color_picked() {	
	color = color_selector.colorselector.rgb;
	if (!change_in_progress){
		config["config_colors_highlight"] = [color.r,color.g,color.b]
		write_config()
	}
}

window.onload = function () {
	color_selector = Metro.getPlugin('@color-selector');
	Metro.getPlugin("@color-selector").colorselector.options.onSelectColor = on_color_picked
}

write_config = function () {
	for (checkbox of $(".config_checkbox")) {
		config[checkbox.children[0].id] = checkbox.children[0].checked
	}

	var changed_config_entries = {}

	for (config_key of Object.keys(config)) {

		if (!((config_key in old_config) && (old_config[config_key] == config[config_key]))) {
			changed_config_entries[config_key] = config[config_key]
		}

	}
	
	if (changed_config_entries) {
		config_change_str = "config_change:" + JSON.stringify(changed_config_entries)
		ws.send(config_change_str)

		old_config = Object.assign({}, config);
	}
}

$(".config_checkbox").change(write_config);