var SerialPort = require("serialport");
var Readline = require("@serialport/parser-readline");
var port = new SerialPort("/dev/tty.usbmodem143301", {
    baudRate: 9600
});
var parser = port.pipe(new Readline({ delimiter: "\r\n" }));
parser.on("data", function (data) {
    if ((data === "Coucou")) {
        console.log("Added Coucou");
    }
    if ((data === "Hello")) {
        console.log("Added Hello");
    }
});
//# sourceMappingURL=index.js.map