
//Constructor
function Pushmi_Pullyu(broker_addr, broker_port, name, in_streams, out_stream) {
	this.name = name;
	this.receive_buffer = new Array();
	this.send_buffer = new Array();

	// MQTT connection
	var mqtt = require('mqtt'), url = require('url');
	this.mqtt_client = mqtt.connect('mqtt://localhost:1883');
	this.mqtt_client.on('connect', function() {
		console.log('Connected to MQTT!')
	});

	// MQTT Subscriptions
	this.mqtt_client.subscribe('test');

	// Receive
	this.mqtt_client.on('message', function(topic, message) {
		receive_buffer.push(message);
		console.log(message.toString());
	});

	this.process_loop();
}

Pushmi_Pullyu.prototype.send = function(message) {

};

Pushmi_Pullyu.prototype.process_loop = function() {
	console.log(this.recieve_buffer);
};

// export the class
var exports = module.exports = Pushmi_Pullyu;