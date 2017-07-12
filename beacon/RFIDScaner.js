var execfile = require('child_process').exec;


var idResult = new Array;

function ExtractRfid(idStr) {
    var ids = idStr.split('\n');
    ids.forEach(function (element) {
        //console.log(element);
        if (idResult.indexOf(element) == -1 && element.length >=40) {
            //console.log(element.length);
            idResult.push(element);
        }
    }, this);
}
//callnum: times to read rfid 
//call interval: interval of each call
function scanRFID(callNum, callInterval, onScanCompleted) {
    idResult=[];
    var read = execfile('./rfidreader', onReadCompleted);

    function onReadCompleted(err, stdout, stderr) {
        callNum -= 1;
        ExtractRfid(stdout);
        if (callNum > 0) {
            setTimeout(function () {
                execfile('./rfidreader', onReadCompleted);
            }, callInterval)
        } else {

            //console.log('reslult: ' + idResult.length)
            //console.log(idResult);
            onScanCompleted(idResult);
        }

    }
}

module.exports.scanRFID = scanRFID;