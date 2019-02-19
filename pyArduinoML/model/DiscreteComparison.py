from pyArduinoML.model.Comparison import Comparison
from .SIGNAL import SIGNAL
from .Sensor import Sensor

class DiscreteComparison(Comparison) :

    def __init__(self, sensor: Sensor, value: SIGNAL):
        self.sensor: str = sensor
        self.value: SIGNAL = value

    def setup(self):
        return "digitalRead(%s) == %s" % (self.sensor.name, str(self.value))
