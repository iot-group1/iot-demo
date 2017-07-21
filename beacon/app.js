var beaconRegion = require('./BeaconRegion');
//var Sound = require('./Beep.js');
var rfidScaner = require('./RFIDScaner.js');
var controller = require('./controller.js');
var exec = require('child_process').exec;
var iotConn = require('./awsiotconnection.js');

var debug = true;
//subscript region event;
var r = beaconRegion.scanRegion(2, 55, 70);
debug ? console.log('Scaning beacons...') : {};
controller.sendCmd('start');

var beaconId;

// enter region event
r.on('enter', function (region) {

    //Sound.beep(300);
	controller.sendCmd('stop');
    debug ? console.log('In Region: ' + region.beaconNameOfRegion + '----------' + region.beacon.id) : {};
	beaconId = region.beacon.id;
    exec('python beep.py');
	debug ? console.log('reading RFID...') : {};
    rfidScaner.scanRFID(8, 1, onScanRfidCompleted)
});

//exit region event;
r.on('exit', function (region) {
    debug ? console.log('Out Region: ' + region.beaconNameOfRegion + '----------' + region.beacon.id) : {};
})

function onScanRfidCompleted(idResult) {
    debug ? console.log(idResult) : {};
    debug ? console.log("Read successful...") : {};
	iotConn.sendMessage('iot_demo',beaconId, new Date().toLocaleString(), idResult.length);
	controller.sendCmd('start');
}
