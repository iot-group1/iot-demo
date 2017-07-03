var beaconRegion = require('./BeaconRegion');
var Sound = require('./Beep.js');
var rfidScaner = require('./RFIDScaner.js');

var debug = true;
//subscript region event;
var r = beaconRegion.scanRegion(3, 65, 75);
debug ? console.log('Scaning beacons...') : {};
// enter region event
r.on('enter', function (region) {

    Sound.beep(300);
    debug ? console.log('In Region: ' + region.beaconNameOfRegion + '----------' + region.beacon.id) : {};
    debug ? console.log('reading RFID...') : {};
    rfidScaner.scanRFID(4, 1000, onScanRfidCompleted)
});

//exit region event;
r.on('exit', function (region) {
    debug ? console.log('Out Region: ' + region.beaconNameOfRegion + '----------' + region.beacon.id) : {};
})

function onScanRfidCompleted(idResult) {
    debug ? console.log(idResult) : {};
    debug ? console.log("Read successful...") : {};
}