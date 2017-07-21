const iotConnection = require('./awsiotconnection.js');

//iotConnection.sendMessage('iot_demo', '989394992934', new Date().toLocaleString(), '15');

setInterval(() => {
    console.log('call');
    iotConnection.sendMessage('iot_demo', '989394992934', new Date().toLocaleString(), '15')
    
}, 5000);

