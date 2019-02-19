from .Sensor import Sensor

class DigitalSensor(Sensor):

    def __init__(self, name: str, pin: int):
        """
        Constructor.

        :param name: String, name of the sensor
        :param pin: Integer, pin where the sensor is connected
        :return:
        """
        Sensor.__init__(self, name, pin)

    def setup(self):
        """
        Arduino code for the setup of the sensor

        :return: String
        """
        return "pinMode(%s, INPUT);" % self.name