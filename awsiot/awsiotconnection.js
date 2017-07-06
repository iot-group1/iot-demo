
const deviceModule = require('/home/pi/node_modules/aws-iot-device-sdk').device;

var device;
const debug = true;
var connectionState;
function createConnection() {

    console.log('connecting AWS...')
    device = deviceModule({
        keyPath: 'pi.private.key',
        certPath: 'pi.cert.pem',
        caPath: 'root-CA.crt',
        clientId: 'burnyspi',
        region: '',
        baseReconnectTimeMs: 4000,
        keepalive: 30,
        protocol: 'mqtts',
        port: 8883,
        host: 'a3jzpapyagk07v.iot.us-east-1.amazonaws.com',
        debug: false
    });

}

function sendMessage(topic, partitionKey, sortKey, messageValue) {

    if (connectionState != 'connected') {
        createConnection();

        device
            .on('connect', function () {
                connectionState = 'connected'
                debug ? console.log(connectionState) : {};
            });
        device
            .on('close', function () {
                connectionState = 'close'
                debug ? console.log(connectionState) : {};
            });
        device
            .on('reconnect', function () {
                connectionState = 'reconnect'
                debug ? console.log(connectionState) : {};
            });
        device
            .on('offline', function () {
                connectionState = 'offline'
                debug ? console.log(connectionState) : {};
            });
        device
            .on('error', function (error) {
                connectionState = 'error'
                debug ? console.log(connectionState, error) : {};
            });
        device
            .on('message', function (topic, payload) {
                connectionState = 'message'
                console.log(connectionState, topic, payload.toString());
            });
    }
    
    device.publish(topic, JSON.stringify({
        beacon_id: partitionKey,
        insert_time: sortKey,
        value: messageValue
    }));
    debug ? console.log("message send") : {};



}
//module.exports.createConnection = createConnection;
module.exports.sendMessage = sendMessage;


