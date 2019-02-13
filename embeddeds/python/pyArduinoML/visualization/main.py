import serial


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
    print("hello")


if __name__ == "__main__":
    serial = initArduino("dev/ttyACM0")
    while True:
        command = ""
        char = ""
        while (char != "\x03"):
            char = serial.read()
            command = command + char
        processData(command)
