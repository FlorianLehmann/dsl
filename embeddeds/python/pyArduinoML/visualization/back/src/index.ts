var SerialPort = require("serialport");
const Readline = require("@serialport/parser-readline");

const port = new SerialPort("/dev/tty.usbmodem143301", {
    baudRate: 9600
});
const parser = port.pipe(new Readline({ delimiter: "\r\n" }));

parser.on("data", (data : string) => {
    if ((data === "Coucou")) {
      console.log("Added Coucou");
    }
    if ((data === "Hello")) {
      console.log("Added Hello");
    }
});