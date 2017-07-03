var gpio = require("gpio");


var gpio4 = gpio.export(18, {

    direction: 'out',

    interval: 200,

    ready: function () {
        gpio4.set(1);
    }
});

function beep(ms) {
    gpio4.set(0);
    setTimeout(function () {
        gpio4.set(1);
    }, ms);
}

module.exports.beep = beep;