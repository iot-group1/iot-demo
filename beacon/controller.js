var net = require('net');

var HOST = '127.0.0.1';
var PORT = 2001;

var STARTCMD_HEX = '00ff130200ff';
var STOPCMD_HEX = '00ff130000ff';

var client = new net.Socket();


var socket = client.connect(PORT, HOST, function(){
	console.log("Connected to the host: " + HOST + " port:" + PORT);
});		

function sendCmd(startOrStop){
	var buffer;
	if(startOrStop == 'start'){
		buffer = new Buffer(STARTCMD_HEX,'hex');
	}else{
		buffer = new Buffer(STOPCMD_HEX, 'hex');
	}
	client.write(buffer);
};


client.on('data', function(data){
	console.log('Data from server is : ' + data);
});

client.on('close', function(){
	console.log("Connection is closed.");
});


module.exports.sendCmd = sendCmd;
