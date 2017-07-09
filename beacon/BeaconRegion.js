var beaconScaner = require('./BeaconScaner')
var EventEmitter = require("events").EventEmitter;
// how many consecutive rssi to change status
var scanNumtoComfirmRegion;
// consider 'in-region' when rssi lower than this
var rssiForRegion;
//consider 'out-region' when rssi greater than this
var rssiOutRegion;
var debug = false;
var CreateRegion = function (name) {
    this.inRegion = false;
    this.scanNumInRegion = 0;
    this.scanNumOutRegion = 0;
    this.beaconNameOfRegion = name;
}
var regions = [new CreateRegion('beetroot'), new CreateRegion('lemon'), new CreateRegion('candy')]

function refreshRegion(beacon, e) {
    var region = findRegionOfBeacon(beacon.name)
    region.beacon = beacon;
    var rssi = Math.abs(beacon.bleacon.rssi);
    if (rssi < rssiForRegion) {
        region.scanNumInRegion += 1;
        region.scanNumOutRegion = 0;
        if(region.inRegion==true){
            resetOtherRegion(region.beaconNameOfRegion)
        }
    }
    if (rssi > rssiOutRegion) {
        region.scanNumInRegion = 0;
        region.scanNumOutRegion += 1;
    }
    // when the received consecutive rssi number meets the condition, send notification
    if (region.scanNumInRegion >= scanNumtoComfirmRegion) {
        comfirmRegion(region, true, e)
    }
    if (region.scanNumOutRegion >= scanNumtoComfirmRegion)
        comfirmRegion(region, false, e);

}

function comfirmRegion(region, isIN, e) {
    if (isIN && !region.inRegion) {
        region.inRegion = true;
        resetOtherRegion(region.beaconNameOfRegion);
        e.emit('enter', region);
    }
    if (!isIN && region.inRegion) {
        region.inRegion = false;
        e.emit('exit', region);
    }
}
function resetOtherRegion(regionName) {
    for (region in regions) {
        if (regions[region].beaconNameOfRegion != regionName) {
            regions[region].inRegion = false;
            regions[region].scanNumInRegion = 0;
            regions[region].scanNumOutRegion = 0;

        }
    }

}

function findRegionOfBeacon(beaconName) {
    for (region in regions) {
        if (regions[region].beaconNameOfRegion == beaconName) {
            return regions[region];
        }
    }
}

function scanRegion(scanNum, rssiIn, rssiOut) {
    rssiForRegion = rssiIn;
    rssiOutRegion = rssiOut;
    scanNumtoComfirmRegion = scanNum;
    var e = new EventEmitter();
    var r = beaconScaner.scanBeacon();
    r.on('scaned', function (beacon) {
        debug ? console.log(beacon.name + '-------' + Math.abs(beacon.bleacon.rssi)) : {};
        refreshRegion(beacon, e);
    })
    return (e);
}
module.exports.scanRegion = scanRegion;