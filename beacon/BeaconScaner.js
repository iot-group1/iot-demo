var Bleacon = require('bleacon');
var EventEmitter = require("events").EventEmitter;

var beaconsId = new Array(3);
beaconsId[0] = 'B9407F30F5F8466EAFF925556B57FE6D2476048904'; //beetroot
beaconsId[1] = 'B9407F30F5F8466EAFF925556B57FE6D2354416095'; //lemon
beaconsId[2] = 'B9407F30F5F8466EAFF925556B57FE6D159756541';  //candy


var beetrootBeacon = new CreateBeacon(beaconsId[0], 'beetroot')
var lemonBeacon = new CreateBeacon(beaconsId[1], 'lemon')
var candyBeacon = new CreateBeacon(beaconsId[2], 'candy')

var beacons = [beetrootBeacon, lemonBeacon, candyBeacon];


function CreateBeacon(sId, sName) {
    this.id = sId;
    this.name = sName;
    this.found = false;
    this.foundTime = 0;
}

function scanBeacon() {
    var e = new EventEmitter();
    Bleacon.startScanning('B9407F30F5F8466EAFF925556B57FE6D'.toLowerCase());
    Bleacon.on('discover', function (bleacon) {
        scanedId = (bleacon.uuid + bleacon.major + bleacon.minor).toUpperCase();
        var scanedBeacon = RefreshBeacon(scanedId, bleacon);
        if (scanedBeacon) {
            e.emit('scaned', scanedBeacon);
        }

    });
    return (e);
}



function RefreshBeacon(id, bleacon) {

    for (tempBeacon in beacons) {
        if (beacons[tempBeacon].id == id) {
            beacons[tempBeacon].bleacon = bleacon;
            beacons[tempBeacon].found = true;
            beacons[tempBeacon].foundTime++;
            return beacons[tempBeacon];
        }

    }


}

module.exports.scanBeacon = scanBeacon;