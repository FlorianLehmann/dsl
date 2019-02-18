import serial
import sys

if sys.platform == 'linux':
    port = '/dev/ttyACM0'
else:
    port = "/dev/tty.usbmodem143120"

def initArduino(serialPort):
    try:
        print("Trying to connect on serial port " + serialPort)
        ser = serial.Serial(serialPort)
        print("Connection successful")
        return ser
    except:
        newSerialPort = input(
            "Connection failed. Input the name of your serial port and press enter : ")
        return initArduino(newSerialPort)


def processData(json):
    print(json)


if __name__ == "__main__":
    serial = initArduino(port)
    serial.flush()
    serial.readline()
    while True:
        try:
            command = serial.readline().decode('utf-8')
        except UnicodeDecodeError as e:
            print(e, file=sys.stderr)
        else:
            processData(command)
